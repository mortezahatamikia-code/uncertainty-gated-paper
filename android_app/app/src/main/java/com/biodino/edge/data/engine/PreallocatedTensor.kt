package com.biodino.edge.data.engine

import android.graphics.Bitmap
import com.biodino.edge.data.image.BitmapUtils
import java.nio.ByteBuffer
import java.nio.ByteOrder
import java.nio.FloatBuffer

/**
 * Reusable direct ByteBuffer for feeding camera frames into ONNX Runtime without allocations.
 */
class PreallocatedTensor(
    val batchSize: Int = 1,
    val channels: Int = 3,
    val height: Int = 224,
    val width: Int = 224
) {
    val totalFloats: Int = batchSize * channels * height * width
    val byteBuffer: ByteBuffer = ByteBuffer.allocateDirect(totalFloats * 4).order(ByteOrder.nativeOrder())
    val floatBuffer: FloatBuffer = byteBuffer.asFloatBuffer()

    private val pixelArray = IntArray(height * width)

    // Standard ImageNet Normalization Constants
    private val meanR = 0.485f
    private val meanG = 0.456f
    private val meanB = 0.406f
    private val invStdR = 1.0f / 0.229f
    private val invStdG = 1.0f / 0.224f
    private val invStdB = 1.0f / 0.225f

    /**
     * Converts, resizes, and normalizes a bitmap directly into the pre-allocated FloatBuffer in NCHW format.
     */
    fun loadFromBitmap(bitmap: Bitmap): FloatBuffer {
        val safeBmp = if (bitmap.config == Bitmap.Config.HARDWARE) {
            bitmap.copy(Bitmap.Config.ARGB_8888, false) ?: bitmap
        } else {
            bitmap
        }

        // Center-crop to square first to avoid geometric stretching and preserve leaf proportions
        val squareBmp = BitmapUtils.centerCropToSquare(safeBmp)

        val scaled = if (squareBmp.width == width && squareBmp.height == height) {
            squareBmp
        } else {
            Bitmap.createScaledBitmap(squareBmp, width, height, true)
        }

        val finalBmp = if (scaled.config == Bitmap.Config.HARDWARE) {
            scaled.copy(Bitmap.Config.ARGB_8888, false) ?: scaled
        } else {
            scaled
        }

        finalBmp.getPixels(pixelArray, 0, width, 0, 0, width, height)

        floatBuffer.clear()
        val numPixels = height * width

        // Channel 0: R
        for (i in 0 until numPixels) {
            val p = pixelArray[i]
            val r = (p shr 16) and 0xFF
            floatBuffer.put(((r / 255.0f) - meanR) * invStdR)
        }
        // Channel 1: G
        for (i in 0 until numPixels) {
            val p = pixelArray[i]
            val g = (p shr 8) and 0xFF
            floatBuffer.put(((g / 255.0f) - meanG) * invStdG)
        }
        // Channel 2: B
        for (i in 0 until numPixels) {
            val p = pixelArray[i]
            val b = p and 0xFF
            floatBuffer.put(((b / 255.0f) - meanB) * invStdB)
        }

        floatBuffer.flip()
        return floatBuffer
    }
}
