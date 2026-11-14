package com.biodino.edge.benchmark

import android.content.Context
import android.graphics.Bitmap
import android.graphics.BitmapFactory

/** Loads the bundled real-leaf benchmark images from assets/images (benchmark build only). */
object BenchmarkImages {
    fun load(context: Context): List<Bitmap> {
        val names = context.assets.list("images") ?: emptyArray()
        val out = ArrayList<Bitmap>()
        for (n in names.sorted()) {
            val lower = n.lowercase()
            if (!lower.endsWith(".jpg") && !lower.endsWith(".png")) continue
            context.assets.open("images/$n").use { ins ->
                BitmapFactory.decodeStream(ins)?.let { out.add(it) }
            }
        }
        return out
    }
}