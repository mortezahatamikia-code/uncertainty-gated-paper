package com.biodino.edge.benchmark

import org.json.JSONArray
import org.json.JSONObject
import kotlin.math.sqrt

/**
 * Small statistics + JSON helpers shared by the on-device benchmark modules.
 * Pure Kotlin / org.json (Android platform), no extra dependencies.
 */
object BenchmarkStats {

    fun mean(a: DoubleArray): Double {
        if (a.isEmpty()) return 0.0
        var s = 0.0
        for (v in a) s += v
        return s / a.size
    }

    fun std(a: DoubleArray): Double {
        if (a.size < 2) return 0.0
        val m = mean(a)
        var s = 0.0
        for (v in a) s += (v - m) * (v - m)
        return sqrt(s / (a.size - 1))
    }

    fun percentile(a: DoubleArray, p: Double): Double {
        if (a.isEmpty()) return 0.0
        val sorted = a.copyOf().also { it.sort() }
        val idx = ((p / 100.0) * (sorted.size - 1)).toInt().coerceIn(0, sorted.size - 1)
        return sorted[idx]
    }

    /** Summarize a latency sample (milliseconds) as mean / std / median / p95 / min / max. */
    fun latencyJson(a: DoubleArray): JSONObject {
        val sorted = a.copyOf().also { it.sort() }
        return JSONObject()
            .put("n", a.size)
            .put("mean", round(mean(a)))
            .put("std", round(std(a)))
            .put("median", round(percentile(a, 50.0)))
            .put("p95", round(percentile(a, 95.0)))
            .put("min", round(if (sorted.isEmpty()) 0.0 else sorted.first()))
            .put("max", round(if (sorted.isEmpty()) 0.0 else sorted.last()))
    }

    fun round(v: Double, digits: Int = 4): Double {
        var f = 1.0
        repeat(digits) { f *= 10 }
        return Math.round(v * f) / f
    }

    fun jsonArrayOf(vararg values: Double): JSONArray {
        val arr = JSONArray()
        for (v in values) arr.put(v)
        return arr
    }
}