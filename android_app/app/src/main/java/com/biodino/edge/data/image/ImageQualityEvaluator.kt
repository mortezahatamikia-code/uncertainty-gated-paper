package com.biodino.edge.data.image

import android.graphics.Bitmap

/**
 * Lightweight, zero-allocation estimator of foliar image sharpness and motion blur.
 * Uses center-crop discrete Laplacian variance.
 */
object ImageQualityEvaluator {

    private const val SAMPLE_SIZE = 64
    private val pixels = IntArray(SAMPLE_SIZE * SAMPLE_SIZE)
    private val gray = FloatArray(SAMPLE_SIZE * SAMPLE_SIZE)

    @Synchronized
    fun isBlurred(bitmap: Bitmap, blurThreshold: Float = 45.0f): Boolean {
        if (bitmap.width < SAMPLE_SIZE || bitmap.height < SAMPLE_SIZE) return false

        // Center crop coordinates
        val startX = (bitmap.width - SAMPLE_SIZE) / 2
        val startY = (bitmap.height - SAMPLE_SIZE) / 2

        val safeBmp = if (bitmap.config == Bitmap.Config.HARDWARE) {
            bitmap.copy(Bitmap.Config.ARGB_8888, false) ?: bitmap
        } else {
            bitmap
        }

        safeBmp.getPixels(pixels, 0, SAMPLE_SIZE, startX, startY, SAMPLE_SIZE, SAMPLE_SIZE)

        // Convert to Luminance
        for (i in 0 until (SAMPLE_SIZE * SAMPLE_SIZE)) {
            val p = pixels[i]
            val r = (p shr 16) and 0xFF
            val g = (p shr 8) and 0xFF
            val b = p and 0xFF
            gray[i] = 0.299f * r + 0.587f * g + 0.114f * b
        }

        // Discrete Laplacian kernel [ 0, 1, 0; 1, -4, 1; 0, 1, 0 ]
        var sum = 0.0
        var sumSq = 0.0
        var count = 0

        for (y in 1 until SAMPLE_SIZE - 1) {
            val rowOffset = y * SAMPLE_SIZE
            val rowAbove = (y - 1) * SAMPLE_SIZE
            val rowBelow = (y + 1) * SAMPLE_SIZE

            for (x in 1 until SAMPLE_SIZE - 1) {
                val center = gray[rowOffset + x]
                val lap = gray[rowAbove + x] +
                        gray[rowBelow + x] +
                        gray[rowOffset + x - 1] +
                        gray[rowOffset + x + 1] -
                        (4.0f * center)

                sum += lap
                sumSq += (lap * lap)
                count++
            }
        }

        if (count == 0) return false
        val mean = sum / count
        val variance = (sumSq / count) - (mean * mean)

        return variance < blurThreshold
    }

    /**
     * Computes the mean luminance in the center crop (0.0 to 255.0).
     */
    @Synchronized
    fun getMeanLuminance(bitmap: Bitmap): Float {
        if (bitmap.width < SAMPLE_SIZE || bitmap.height < SAMPLE_SIZE) return 128.0f

        val startX = (bitmap.width - SAMPLE_SIZE) / 2
        val startY = (bitmap.height - SAMPLE_SIZE) / 2

        val safeBmp = if (bitmap.config == Bitmap.Config.HARDWARE) {
            bitmap.copy(Bitmap.Config.ARGB_8888, false) ?: bitmap
        } else {
            bitmap
        }

        safeBmp.getPixels(pixels, 0, SAMPLE_SIZE, startX, startY, SAMPLE_SIZE, SAMPLE_SIZE)

        var sumLum = 0.0
        val total = SAMPLE_SIZE * SAMPLE_SIZE
        for (i in 0 until total) {
            val p = pixels[i]
            val r = (p shr 16) and 0xFF
            val g = (p shr 8) and 0xFF
            val b = p and 0xFF
            sumLum += (0.299 * r + 0.587 * g + 0.114 * b)
        }
        return (sumLum / total).toFloat()
    }

    /**
     * Detects pitch-black scenes, covered lenses, or severe underexposure.
     * Threshold is 22.0f out of 255.0 (covered lens is 0-5, indoor foliage is > 40).
     */
    fun isTooDark(bitmap: Bitmap, darkThreshold: Float = 22.0f): Boolean {
        return getMeanLuminance(bitmap) < darkThreshold
    }
}
