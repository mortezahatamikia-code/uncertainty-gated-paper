package com.biodino.edge.benchmark

import android.app.ActivityManager
import android.content.Context
import android.graphics.Bitmap
import android.os.Build
import android.os.Debug
import android.os.PowerManager
import android.os.SystemClock
import org.json.JSONObject

/**
 * On-device inference benchmark: model load time, peak RAM, per-stage end-to-end
 * latency (cascade and Tier-2-on-all), and a sustained loop for thermal/energy.
 *
 * All latency samples use SystemClock.elapsedRealtimeNanos() (monotonic).
 */
class DeviceBenchmark(private val context: Context) {

    private val tag = "BioDinoBench"

    private fun pssMb(): Double = Debug.getPss() / 1024.0
    private fun nativeHeapMb(): Double = Debug.getNativeHeapAllocatedSize() / (1024.0 * 1024.0)

    private fun thermalStatus(): Int {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) return -1
        val pm = context.getSystemService(Context.POWER_SERVICE) as? PowerManager ?: return -1
        return try { pm.currentThermalStatus } catch (_: Exception) { -1 }
    }

    private fun loadImages(): List<Bitmap> = BenchmarkImages.load(context)

    fun deviceJson(): JSONObject {
        val am = context.getSystemService(Context.ACTIVITY_SERVICE) as? ActivityManager
        val memInfo = ActivityManager.MemoryInfo()
        am?.getMemoryInfo(memInfo)
        val soc = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
            "${Build.SOC_MANUFACTURER} ${Build.SOC_MODEL}".trim()
        } else "unknown"
        return JSONObject()
            .put("manufacturer", Build.MANUFACTURER)
            .put("model", Build.MODEL)
            .put("device", Build.DEVICE)
            .put("soc", soc)
            .put("android_release", Build.VERSION.RELEASE)
            .put("sdk_int", Build.VERSION.SDK_INT)
            .put("abi", Build.SUPPORTED_ABIS.firstOrNull() ?: "unknown")
            .put("cores", Runtime.getRuntime().availableProcessors())
            .put("total_ram_mb", BenchmarkStats.round(memInfo.totalMem / (1024.0 * 1024.0), 1))
            .put("onnxruntime_version", "1.18.0")
            .put("cpu_threads_intra", 4)
            .put("cpu_threads_inter", 2)
            .put("nnapi_enabled", false)
            .put("quantization", "INT8")
    }

    private data class Iter(
        val pre: Double, val enc1: Double, val gate: Double,
        val enc2: Double, val decision: Double, val escalated: Boolean
    )

    private fun runOnce(s: EdgeSessions, bmp: Bitmap, tau: Float, withTier2: Boolean): Iter {
        val t0 = SystemClock.elapsedRealtimeNanos()
        val buf = s.preprocess(bmp)
        val input = s.inputTensor(buf)
        val t1 = SystemClock.elapsedRealtimeNanos()
        val pre = (t1 - t0) / 1e6

        val o1 = s.runTier1(input)
        val t2 = SystemClock.elapsedRealtimeNanos()
        val enc1 = (t2 - t1) / 1e6

        val escalate = o1.confidence < tau
        val t3 = SystemClock.elapsedRealtimeNanos()
        val gate = (t3 - t2) / 1e6

        var enc2 = 0.0
        var finalProbs = o1.probs
        var t4 = t3
        if (withTier2 && s.tier2Available) {
            val o2 = s.runTier2(input, o1.dino)
            finalProbs = o2.probs
            t4 = SystemClock.elapsedRealtimeNanos()
            enc2 = (t4 - t3) / 1e6
        }

        // Decision: argmax over the active probability vector.
        var best = 0
        for (k in finalProbs.indices) if (finalProbs[k] > finalProbs[best]) best = k
        val t5 = SystemClock.elapsedRealtimeNanos()
        val decision = (t5 - t4) / 1e6

        input.close()
        return Iter(pre, enc1, gate, enc2, decision, escalate)
    }

    fun run(
        nIters: Int, warmup: Int, sustainedSeconds: Int, tau: Float,
        log: (String) -> Unit,
        adaptation: ((EdgeSessions, List<Bitmap>) -> JSONObject)? = null
    ): JSONObject {
        val images = loadImages()
        require(images.isNotEmpty()) { "No benchmark images found in assets/images" }
        log("Loaded ${images.size} benchmark images")

        val idlePss = pssMb()
        val sessions = EdgeSessions(context)
        sessions.load()
        val afterT1Pss = pssMb()
        log("Tier-1 load: read ${sessions.tier1AssetReadMs} ms + session ${sessions.tier1SessionCreateMs} ms")
        var afterT2Pss = afterT1Pss
        if (sessions.tier2Available) {
            afterT2Pss = pssMb()
            log("Tier-2 load (${sessions.tier2Source}): read ${sessions.tier2FileReadMs} ms + session ${sessions.tier2SessionCreateMs} ms")
        } else {
            log("WARNING: Tier-2 companion not found; escalation stages will be skipped")
        }

        val withTier2 = sessions.tier2Available
        // Phase 1 (cool device): warmup + latency loop. Thermal state recorded so the
        // per-query numbers can be qualified. Adaptation runs next, sustained loop LAST,
        // so the heat soak never contaminates the latency or algebra measurements.
        val thermalLatencyStart = thermalStatus()
        // Warmup (JIT + ORT kernel warm-up), excluded from statistics.
        repeat(warmup) { runOnce(sessions, images[it % images.size], tau, withTier2) }

        val pre = DoubleArray(nIters); val enc1 = DoubleArray(nIters)
        val gate = DoubleArray(nIters); val enc2 = DoubleArray(nIters)
        val dec = DoubleArray(nIters); val e2eCascade = DoubleArray(nIters); val e2eAll = DoubleArray(nIters)
        var fastExit = 0
        var peakPss = afterT2Pss; var peakNative = nativeHeapMb()

        for (i in 0 until nIters) {
            val it = runOnce(sessions, images[i % images.size], tau, withTier2)
            pre[i] = it.pre; enc1[i] = it.enc1; gate[i] = it.gate; enc2[i] = it.enc2; dec[i] = it.decision
            val cascade = it.pre + it.enc1 + it.gate + (if (it.escalated) it.enc2 else 0.0) + it.decision
            val all = it.pre + it.enc1 + it.gate + it.enc2 + it.decision
            e2eCascade[i] = cascade; e2eAll[i] = all
            if (!it.escalated) fastExit++
            val p = pssMb(); if (p > peakPss) peakPss = p
            val nh = nativeHeapMb(); if (nh > peakNative) peakNative = nh
        }
        log("Latency loop done: $nIters iters, fast-exit ${100.0 * fastExit / nIters}%")
        val thermalLatencyEnd = thermalStatus()

        // Phase 2: adaptation breakdown on the (still cool) device, before the heat soak.
        val adaptationJson = adaptation?.invoke(sessions, images)

        // Phase 3 (last): sustained loop for thermal throttling + energy (batterystats parsed externally).
        val thermalStart = thermalStatus()
        var thermalMax = thermalStart
        var sustainedIters = 0
        val sustainStart = SystemClock.elapsedRealtime()
        val sustainMs = sustainedSeconds * 1000L
        var lastSample = sustainStart
        while (SystemClock.elapsedRealtime() - sustainStart < sustainMs) {
            runOnce(sessions, images[sustainedIters % images.size], tau, withTier2)
            sustainedIters++
            val now = SystemClock.elapsedRealtime()
            if (now - lastSample >= 5000L) {
                val th = thermalStatus(); if (th > thermalMax) thermalMax = th
                val p = pssMb(); if (p > peakPss) peakPss = p
                lastSample = now
            }
        }
        val sustainWall = (SystemClock.elapsedRealtime() - sustainStart) / 1000.0
        val thermalEnd = thermalStatus()
        log("Sustained loop: $sustainedIters iters in ${BenchmarkStats.round(sustainWall, 1)} s")

        sessions.close()

        val loadJson = JSONObject()
            .put("tier1_asset_read_ms", BenchmarkStats.round(sessions.tier1AssetReadMs))
            .put("tier1_session_create_ms", BenchmarkStats.round(sessions.tier1SessionCreateMs))
            .put("tier1_total_ms", BenchmarkStats.round(sessions.tier1AssetReadMs + sessions.tier1SessionCreateMs))
            .put("tier2_available", sessions.tier2Available)
            .put("tier2_source", sessions.tier2Source)
            .put("tier2_file_read_ms", BenchmarkStats.round(sessions.tier2FileReadMs))
            .put("tier2_session_create_ms", BenchmarkStats.round(sessions.tier2SessionCreateMs))
            .put("tier2_total_ms", BenchmarkStats.round(sessions.tier2FileReadMs + sessions.tier2SessionCreateMs))

        val memJson = JSONObject()
            .put("idle_pss_mb", BenchmarkStats.round(idlePss, 2))
            .put("after_tier1_load_pss_mb", BenchmarkStats.round(afterT1Pss, 2))
            .put("after_tier2_load_pss_mb", BenchmarkStats.round(afterT2Pss, 2))
            .put("peak_pss_mb", BenchmarkStats.round(peakPss, 2))
            .put("peak_native_heap_mb", BenchmarkStats.round(peakNative, 2))

        val tier1Json = JSONObject()
            .put("preprocess_ms", BenchmarkStats.latencyJson(pre))
            .put("encoder_ms", BenchmarkStats.latencyJson(enc1))
            .put("gate_ms", BenchmarkStats.latencyJson(gate))
            .put("total_ms", BenchmarkStats.latencyJson(DoubleArray(nIters) { pre[it] + enc1[it] + gate[it] + dec[it] }))
        val tier2Json = JSONObject()
            .put("incremental_ms", BenchmarkStats.latencyJson(enc2))
            .put("note", "BioCLIP encoder + 896-D Fisher + text fusion are one baked ONNX graph")

        val latencyJson = JSONObject()
            .put("tier1", tier1Json)
            .put("tier2", tier2Json)
            .put("decision_ms", BenchmarkStats.latencyJson(dec))
            .put("cascade_end_to_end_ms", BenchmarkStats.latencyJson(e2eCascade))
            .put("tier2_on_all_end_to_end_ms", BenchmarkStats.latencyJson(e2eAll))
            .put("fast_exit_fraction", BenchmarkStats.round(fastExit.toDouble() / nIters))
            .put("tau", tau.toDouble())
            .put("thermal_start", thermalLatencyStart)
            .put("thermal_end", thermalLatencyEnd)

        val sustainedJson = JSONObject()
            .put("iterations", sustainedIters)
            .put("wall_seconds", BenchmarkStats.round(sustainWall, 2))
            .put("throughput_fps", BenchmarkStats.round(sustainedIters / sustainWall, 2))
            .put("thermal_start", thermalStart)
            .put("thermal_end", thermalEnd)
            .put("thermal_max", thermalMax)
            .put("energy_method", "batterystats (parsed externally by run_device_benchmark.ps1)")

        val result = JSONObject()
            .put("device", deviceJson())
            .put("model_load", loadJson)
            .put("memory", memJson)
            .put("latency", latencyJson)
            .put("sustained", sustainedJson)
        if (adaptationJson != null) result.put("adaptation", adaptationJson)
        return result
    }
}