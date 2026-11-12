package com.biodino.edge.data.network

import android.content.Context
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import java.io.File
import java.io.FileOutputStream
import java.io.InputStream
import java.net.HttpURLConnection
import java.net.URL

/**
 * Handles downloading, verifying, caching, and activating custom / companion ONNX models
 * from GitHub Releases or remote URLs directly into private internal storage.
 */
object ModelDownloadManager {

    /**
     * GitHub raw URL for Tier-2 companion model (biodino_companion_int8.onnx, 85.3 MB).
     * Sourced from pipeline/export_edge_models.py.
     */
    const val URL_COMPANION_MODEL: String =
        "https://github.com/mortezahatamikia-code/uncertainty-gated-paper/raw/master/biodino_companion_int8.onnx"

    const val URL_COMPANION_85MB: String = URL_COMPANION_MODEL
    const val COMPANION_MODEL_EXACT_SIZE_MB: Float = 85.3f

    const val DEFAULT_GITHUB_MODEL_URL: String = URL_COMPANION_MODEL

    /**
     * Normalizes GitHub URLs: converts web preview links (/blob/) into direct raw binary links (/raw/).
     */
    fun normalizeDownloadUrl(rawUrl: String): String {
        var url = rawUrl.trim()
        if (url.contains("github.com") && url.contains("/blob/")) {
            url = url.replaceFirst("/blob/", "/raw/")
        }
        return url
    }

    private const val MODEL_DIR: String = "models"
    private const val CUSTOM_MODEL_FILENAME: String = "biodino_custom_model.onnx"
    private const val TEMP_MODEL_FILENAME: String = "biodino_custom_model.onnx.tmp"
    private const val MIN_VALID_MODEL_BYTES: Long = 5 * 1024 * 1024 // Minimum 5 MB for a valid model

    fun getModelDirectory(context: Context): File {
        val dir = File(context.filesDir, MODEL_DIR)
        if (!dir.exists()) {
            dir.mkdirs()
        }
        return dir
    }

    fun getCustomModelFile(context: Context): File {
        return File(getModelDirectory(context), CUSTOM_MODEL_FILENAME)
    }

    fun isCustomModelActive(context: Context): Boolean {
        val file = getCustomModelFile(context)
        return file.exists() && file.isFile && file.length() >= MIN_VALID_MODEL_BYTES
    }

    fun getCustomModelSizeMb(context: Context): Float {
        val file = getCustomModelFile(context)
        return if (file.exists()) {
            file.length() / (1024f * 1024f)
        } else {
            0f
        }
    }

    fun deleteCustomModel(context: Context): Boolean {
        val file = getCustomModelFile(context)
        return if (file.exists()) {
            file.delete()
        } else {
            true
        }
    }

    /**
     * Downloads model binary from remote URL with support for HTTP redirects (standard in GitHub Releases),
     * atomic temporary write, and real-time progress callbacks.
     */
    suspend fun downloadModel(
        context: Context,
        downloadUrl: String,
        onProgress: (downloadedBytes: Long, totalBytes: Long, progress: Float) -> Unit
    ): Result<File> = withContext(Dispatchers.IO) {
        var connection: HttpURLConnection? = null
        var inputStream: InputStream? = null
        var outputStream: FileOutputStream? = null
        val tempFile = File(getModelDirectory(context), TEMP_MODEL_FILENAME)
        val targetFile = getCustomModelFile(context)

        try {
            var currentUrl = normalizeDownloadUrl(downloadUrl)
            var redirects = 0
            val maxRedirects = 6

            // Follow HTTP redirects (301, 302, 303, 307, 308 - crucial for GitHub Releases assets)
            while (redirects < maxRedirects) {
                val url = URL(currentUrl)
                connection = (url.openConnection() as HttpURLConnection).apply {
                    connectTimeout = 20_000
                    readTimeout = 60_000
                    instanceFollowRedirects = false
                    setRequestProperty("User-Agent", "BioDINO-Edge-Android")
                    setRequestProperty("Accept", "*/*")
                }

                val responseCode = connection.responseCode
                if (responseCode in 300..399) {
                    val newLocation = connection.getHeaderField("Location")
                        ?: throw IllegalStateException("Redirected with empty Location header (HTTP $responseCode)")
                    connection.disconnect()
                    currentUrl = if (newLocation.startsWith("http")) {
                        newLocation
                    } else {
                        URL(url, newLocation).toString()
                    }
                    redirects++
                } else if (responseCode == HttpURLConnection.HTTP_OK) {
                    break
                } else {
                    throw IllegalStateException("Server returned HTTP $responseCode: ${connection.responseMessage}")
                }
            }

            val conn = connection ?: throw IllegalStateException("Failed to establish HTTP connection")
            val contentLength = conn.contentLengthLong

            if (tempFile.exists()) {
                tempFile.delete()
            }

            inputStream = conn.inputStream
            outputStream = FileOutputStream(tempFile)

            val buffer = ByteArray(64 * 1024) // 64 KB buffer
            var totalBytesRead = 0L
            var bytesRead: Int

            while (inputStream.read(buffer).also { bytesRead = it } != -1) {
                outputStream.write(buffer, 0, bytesRead)
                totalBytesRead += bytesRead

                val progress = if (contentLength > 0) {
                    (totalBytesRead.toFloat() / contentLength).coerceIn(0f, 1f)
                } else {
                    0f
                }
                onProgress(totalBytesRead, contentLength, progress)
            }

            outputStream.flush()
            outputStream.close()
            outputStream = null
            inputStream.close()
            inputStream = null

            // Validate downloaded payload size
            if (tempFile.length() < MIN_VALID_MODEL_BYTES) {
                tempFile.delete()
                return@withContext Result.failure(
                    IllegalStateException("Downloaded file is too small (${tempFile.length()} bytes). Verify URL.")
                )
            }

            // Atomic rename
            if (targetFile.exists()) {
                targetFile.delete()
            }
            val renamed = tempFile.renameTo(targetFile)
            if (!renamed) {
                // Fallback copy if rename fails across partitions
                tempFile.copyTo(targetFile, overwrite = true)
                tempFile.delete()
            }

            onProgress(targetFile.length(), targetFile.length(), 1.0f)
            Result.success(targetFile)
        } catch (e: Exception) {
            if (tempFile.exists()) {
                tempFile.delete()
            }
            Result.failure(e)
        } finally {
            try { outputStream?.close() } catch (_: Exception) {}
            try { inputStream?.close() } catch (_: Exception) {}
            try { connection?.disconnect() } catch (_: Exception) {}
        }
    }
}

