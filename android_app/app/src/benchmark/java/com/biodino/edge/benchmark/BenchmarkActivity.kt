package com.biodino.edge.benchmark

import android.app.Activity
import android.os.Bundle
import android.os.SystemClock
import android.text.method.ScrollingMovementMethod
import android.util.Log
import android.view.WindowManager
import android.widget.ScrollView
import android.widget.TextView
import org.json.JSONObject
import java.io.File
import java.text.SimpleDateFormat
import java.util.Date
import java.util.Locale
import java.util.TimeZone

/**
 * Research benchmark entry point (benchmark build type only). Launch via adb:
 *
 *   adb shell am start -n com.biodino.edge/.benchmark.BenchmarkActivity \
 *       --ei n_iters 100 --ei sustained_seconds 600
 *
 * Intent extras (all optional):
 *   n_iters            latency samples (default 100)
 *   warmup             warm-up iterations excluded from stats (default 10)
 *   sustained_seconds  sustained-loop duration for thermal/energy (default 120)
 *   tau                gate threshold (default 0.35)
 *   adaptation_views   support views for the adaptation breakdown (default 440)
 *   adaptation_repeats algebra repeat count (default 5)
 *   run_adaptation     0 to skip the adaptation benchmark (default 1)
 *
 * Writes benchmark_report.json to getExternalFilesDir(null) and logs BENCHMARK_DONE.
 */
class BenchmarkActivity : Activity() {

    private val tag = "BioDinoBench"
    private lateinit var status: TextView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        window.addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON)
        status = TextView(this).apply {
            textSize = 12f
            setPadding(24, 24, 24, 24)
            movementMethod = ScrollingMovementMethod()
            text = "BioDINO-Edge on-device benchmark\nStarting...\n"
        }
        setContentView(ScrollView(this).apply { addView(status) })

        val nIters = intent.getIntExtra("n_iters", 100)
        val warmup = intent.getIntExtra("warmup", 10)
        val sustainedSeconds = intent.getIntExtra("sustained_seconds", 120)
        val tau = intent.getFloatExtra("tau", 0.35f)
        val adaptationViews = intent.getIntExtra("adaptation_views", 440)
        val adaptationRepeats = intent.getIntExtra("adaptation_repeats", 5)
        val runAdaptation = intent.getIntExtra("run_adaptation", 1) == 1
        val cooldownSeconds = intent.getIntExtra("cooldown_seconds", 45)

        Thread {
            val report = JSONObject()
            try {
                log("Device: ${android.os.Build.MANUFACTURER} ${android.os.Build.MODEL}")
                log("Config: iters=$nIters warmup=$warmup sustained=${sustainedSeconds}s tau=$tau cooldown=${cooldownSeconds}s")
                // Adaptation runs between the latency loop and the sustained heat soak (see
                // DeviceBenchmark), on a cool device, with a cool-down before algebra timing.
                val deviceResult = DeviceBenchmark(this).run(
                    nIters, warmup, sustainedSeconds, tau, { log(it) },
                    if (runAdaptation) { sess, imgs ->
                        if (sess.tier2Available) {
                            AdaptationBenchmark(this, sess, imgs)
                                .run(adaptationViews, 11, adaptationRepeats, cooldownSeconds) { log(it) }
                        } else {
                            log("Adaptation skipped: no Tier-2 companion")
                            JSONObject().put("skipped", "Tier-2 companion not present; push biodino_companion_int8.onnx")
                        }
                    } else null
                )
                for (key in deviceResult.keys()) report.put(key, deviceResult.get(key))

                report.put("schema", "biodino_edge_device_benchmark_v1")
                report.put("timestamp_utc", utcNow())
                report.put("config", JSONObject()
                    .put("n_iters", nIters).put("warmup", warmup)
                    .put("sustained_seconds", sustainedSeconds).put("tau", tau.toDouble())
                    .put("adaptation_views", adaptationViews).put("adaptation_repeats", adaptationRepeats)
                    .put("cooldown_seconds", cooldownSeconds))
                report.put("status", "complete")
            } catch (e: Exception) {
                Log.e(tag, "benchmark failed", e)
                report.put("status", "error")
                report.put("error", "${e.javaClass.simpleName}: ${e.message}")
                log("ERROR: ${e.message}")
            }

            val outFile = File(getExternalFilesDir(null), "benchmark_report.json")
            try {
                outFile.writeText(report.toString(2))
                log("Report written: ${outFile.absolutePath}")
            } catch (e: Exception) {
                Log.e(tag, "write failed", e)
            }
            Log.i(tag, "BENCHMARK_DONE ${outFile.absolutePath}")
            log("BENCHMARK_DONE")
        }.start()
    }

    private fun utcNow(): String {
        val fmt = SimpleDateFormat("yyyy-MM-dd'T'HH:mm:ss'Z'", Locale.US)
        fmt.timeZone = TimeZone.getTimeZone("UTC")
        return fmt.format(Date())
    }

    private fun log(msg: String) {
        Log.i(tag, msg)
        val stamp = SystemClock.elapsedRealtime() / 1000
        runOnUiThread { status.append("[${stamp}s] $msg\n") }
    }
}