package com.biodino.edge.data.image

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.graphics.ImageDecoder
import android.graphics.Matrix
import android.media.ExifInterface
import android.net.Uri
import android.os.Build

/**
 * Robust image decoding utilities designed to safely ingest foliage photos from
 * Android gallery, downloads, cloud storage, and camera rolls without OOM or Config#HARDWARE crashes.
 */
object BitmapUtils {

    /**
     * Decodes a Uri into a mutable software ARGB_8888 Bitmap, automatically correcting
     * EXIF rotation and constraining maximum dimensions to avoid memory bloat.
     */
    fun decodeSoftwareBitmap(context: Context, uri: Uri, maxDimension: Int = 1200): Bitmap? {
        val cr = context.contentResolver

        // 1. Read byte payload to prevent stream-reset failures on non-seekable ContentProviders
        val rawBytes: ByteArray = try {
            cr.openInputStream(uri)?.use { it.readBytes() } ?: return null
        } catch (_: Throwable) {
            return null
        }

        if (rawBytes.isEmpty()) return null

        // 2. Decode bitmap safely
        val decodedBitmap: Bitmap? = try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                val source = ImageDecoder.createSource(rawBytes.inputStream().let { cr.openInputStream(uri) ?: it }.let {
                    // Use ImageDecoder with ByteBuffer
                    java.nio.ByteBuffer.wrap(rawBytes)
                })
                ImageDecoder.decodeBitmap(source) { decoder, info, _ ->
                    decoder.allocator = ImageDecoder.ALLOCATOR_SOFTWARE
                    decoder.isMutableRequired = true
                    val maxSide = maxOf(info.size.width, info.size.height)
                    if (maxSide > maxDimension) {
                        decoder.setTargetSampleSize(maxOf(1, maxSide / maxDimension))
                    }
                }
            } else {
                val boundsOptions = BitmapFactory.Options().apply { inJustDecodeBounds = true }
                BitmapFactory.decodeByteArray(rawBytes, 0, rawBytes.size, boundsOptions)
                val maxSide = maxOf(boundsOptions.outWidth, boundsOptions.outHeight)
                val sampleSize = if (maxSide > maxDimension) maxOf(1, maxSide / maxDimension) else 1

                val decodeOptions = BitmapFactory.Options().apply {
                    inSampleSize = sampleSize
                    inPreferredConfig = Bitmap.Config.ARGB_8888
                }
                BitmapFactory.decodeByteArray(rawBytes, 0, rawBytes.size, decodeOptions)
            }
        } catch (_: Throwable) {
            // Ultimate fallback
            try {
                BitmapFactory.decodeByteArray(rawBytes, 0, rawBytes.size)
            } catch (_: Throwable) {
                null
            }
        }

        if (decodedBitmap == null) return null

        // 3. Guarantee software bitmap (no Config#HARDWARE)
        val softwareBmp = if (decodedBitmap.config == Bitmap.Config.HARDWARE) {
            decodedBitmap.copy(Bitmap.Config.ARGB_8888, false) ?: decodedBitmap
        } else {
            decodedBitmap
        }

        // 4. Correct EXIF Orientation if present
        return try {
            val exifInterface = ExifInterface(rawBytes.inputStream())
            val orientation = exifInterface.getAttributeInt(
                ExifInterface.TAG_ORIENTATION,
                ExifInterface.ORIENTATION_NORMAL
            )
            val matrix = Matrix()
            when (orientation) {
                ExifInterface.ORIENTATION_ROTATE_90 -> matrix.postRotate(90f)
                ExifInterface.ORIENTATION_ROTATE_180 -> matrix.postRotate(180f)
                ExifInterface.ORIENTATION_ROTATE_270 -> matrix.postRotate(270f)
                ExifInterface.ORIENTATION_FLIP_HORIZONTAL -> matrix.postScale(-1f, 1f)
                ExifInterface.ORIENTATION_FLIP_VERTICAL -> matrix.postScale(1f, -1f)
                else -> return softwareBmp
            }
            Bitmap.createBitmap(softwareBmp, 0, 0, softwareBmp.width, softwareBmp.height, matrix, true)
        } catch (_: Throwable) {
            softwareBmp
        }
    }

    /**
     * Crops the center square of a bitmap so that width == height, preserving geometric aspect ratio
     * and preventing leaf/lesion stretching during neural network inference.
     */
    fun centerCropToSquare(bitmap: Bitmap): Bitmap {
        val width = bitmap.width
        val height = bitmap.height
        if (width == height) return bitmap
        val size = minOf(width, height)
        val x = (width - size) / 2
        val y = (height - size) / 2
        return Bitmap.createBitmap(bitmap, x, y, size, size)
    }
}
