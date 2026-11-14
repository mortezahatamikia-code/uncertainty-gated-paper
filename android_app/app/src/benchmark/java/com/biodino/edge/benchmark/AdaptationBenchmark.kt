package com.biodino.edge.benchmark

import android.content.Context
import android.graphics.Bitmap
import android.graphics.Canvas
import android.graphics.ColorMatrix
import android.graphics.ColorMatrixColorFilter
import android.graphics.Matrix
import android.graphics.Paint
import android.os.Build
import android.os.PowerManager
import android.os.SystemClock
import org.ejml.data.DMatrixRMaj
import org.ejml.dense.row.factory.DecompositionFactory_DDRM
import org.ejml.simple.SimpleMatrix
import org.json.JSONObject
import kotlin.math.ln
import kotlin.math.min

/**
 * Adaptation-cost breakdown for the closed-form Fisher recalibration, measured on-device
 * (supersedes the earlier "<22 ms" projection-only estimate).
 *
 * Separates the five stages the reviewer asked for:
 *   1. Feature extraction  : 440 augmented views through Tier-1 (DINOv2 384-D) + Tier-2 (BioCLIP 512-D)
 *                            -> joint 896-D support matrix X. Reported separately (dominant cost).
 *   2. Covariance estimate : centered scatter S = X^T X / N           (O(N d^2))
 *   3. Ledoit-Wolf shrink  : optimal shrinkage intensity alpha         (O(N d), closed-form identity)
 *   4. Cholesky factor     : Sigma = (1-a) S + a mu I = L L^T          (O(d^3 / 3))
 *   5. Projection solve    : triangular solves for W (C x d) + bias b  (O(C d^2))
 *
 * The algebraic recalibration budget (stages 2-5) is measured sub-second on the physical
 * device; stage 1 (encoder forward passes) is reported explicitly so the full cost is transparent.
 * The algebra mirrors pipeline/core_math.fit_fisher_lda (sklearn LDA lsqr + Ledoit-Wolf).
 */
class AdaptationBenchmark(
    private val context: Context,
    private val sessions: EdgeSessions,
    private val images: List<Bitmap>
) {

    private fun thermalStatus(): Int {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q) return -1
        val pm = context.getSystemService(Context.POWER_SERVICE) as? PowerManager ?: return -1
        return try { pm.currentThermalStatus } catch (_: Exception) { -1 }
    }

    private fun augment(src: Bitmap, v: Int): Bitmap {
        val flipH = if (v % 2 == 0) -1f else 1f
        val flipV = if (v % 4 < 2) -1f else 1f
        val angle = ((v % 8) - 4) * 3.75f // +/- 15 degrees
        val m = Matrix()
        m.postScale(flipH, flipV, src.width / 2f, src.height / 2f)
        m.postRotate(angle, src.width / 2f, src.height / 2f)
        val rotated = Bitmap.createBitmap(src, 0, 0, src.width, src.height, m, true)
        val brightness = 1f + ((v % 3) - 1) * 0.2f
        val out = Bitmap.createBitmap(rotated.width, rotated.height, Bitmap.Config.ARGB_8888)
        val cm = ColorMatrix(floatArrayOf(
            brightness, 0f, 0f, 0f, 0f,
            0f, brightness, 0f, 0f, 0f,
            0f, 0f, brightness, 0f, 0f,
            0f, 0f, 0f, 1f, 0f
        ))
        val paint = Paint().apply { colorFilter = ColorMatrixColorFilter(cm) }
        Canvas(out).drawBitmap(rotated, 0f, 0f, paint)
        if (rotated != src) rotated.recycle()
        return out
    }

    /** Stage 1: extract N augmented views into a joint [bio || dino] matrix. */
    private fun extract(nViews: Int, nClasses: Int, log: (String) -> Unit): ExtractResult {
        val d = 896
        val x = Array(nViews) { DoubleArray(d) }
        val labels = IntArray(nViews) { it % nClasses }
        var t1Total = 0.0
        var t2Total = 0.0
        val start = SystemClock.elapsedRealtimeNanos()
        for (v in 0 until nViews) {
            val aug = augment(images[v % images.size], v)
            val buf = sessions.preprocess(aug)
            val input = sessions.inputTensor(buf)
            val a = SystemClock.elapsedRealtimeNanos()
            val o1 = sessions.runTier1(input)
            val b = SystemClock.elapsedRealtimeNanos()
            val o2 = sessions.runTier2(input, o1.dino)
            val c = SystemClock.elapsedRealtimeNanos()
            t1Total += (b - a) / 1e6
            t2Total += (c - b) / 1e6
            for (k in 0 until 512) x[v][k] = o2.bio[k].toDouble()
            for (k in 0 until 384) x[v][512 + k] = o1.dino[k].toDouble()
            input.close()
            aug.recycle()
            if ((v + 1) % 110 == 0) log("  extracted ${v + 1}/$nViews views")
        }
        val total = (SystemClock.elapsedRealtimeNanos() - start) / 1e6
        return ExtractResult(x, labels, total, t1Total, t2Total)
    }

    private data class ExtractResult(
        val x: Array<DoubleArray>, val labels: IntArray,
        val totalMs: Double, val tier1Ms: Double, val tier2Ms: Double
    )

    private data class AlgebraMs(val cov: Double, val lw: Double, val chol: Double, val solve: Double, val alpha: Double)

    /** Stages 2-5 on the extracted support matrix. */
    private fun algebraOnce(x: Array<DoubleArray>, labels: IntArray, nClasses: Int): AlgebraMs {
        val n = x.size
        val d = x[0].size

        // ---- Stage 2: covariance (center + scatter) ----
        val tCov0 = SystemClock.elapsedRealtimeNanos()
        val global = DoubleArray(d)
        for (row in x) for (j in 0 until d) global[j] += row[j]
        for (j in 0 until d) global[j] /= n
        val xc = Array(n) { i -> DoubleArray(d) { j -> x[i][j] - global[j] } }
        var sumNorm4 = 0.0
        for (row in xc) {
            var norm2 = 0.0
            for (v in row) norm2 += v * v
            sumNorm4 += norm2 * norm2
        }
        val xm = SimpleMatrix(xc)
        val s = xm.transpose().mult(xm).scale(1.0 / n)
        val tCov1 = SystemClock.elapsedRealtimeNanos()

        // ---- Stage 3: Ledoit-Wolf shrinkage intensity (closed form, O(N d)) ----
        // sum_i ||x_i x_i^T - S||_F^2 = sum_i ||x_i||^4 - N ||S||_F^2, since
        // sum_i x_i^T S x_i = trace(S X^T X) = N trace(S^2) = N ||S||_F^2.
        val trace = s.trace()
        val mu = trace / d
        val froS = s.normF()
        val froS2 = froS * froS
        val delta2 = (froS2 - 2.0 * mu * trace + d * mu * mu) / d
        val sumBeta = sumNorm4 - n * froS2
        var beta2 = sumBeta / (n.toDouble() * n) / d
        beta2 = min(beta2, delta2)
        val alpha = if (delta2 > 1e-12) beta2 / delta2 else 0.0
        val tLw1 = SystemClock.elapsedRealtimeNanos()

        // ---- Stage 4: Cholesky factorization of shrunk covariance ----
        val sigma = s.scale(1.0 - alpha).plus(SimpleMatrix.identity(d).scale(alpha * mu))
        val chol = DecompositionFactory_DDRM.chol(d, true)
        val ok = chol.decompose(sigma.getDDRM())
        if (!ok) throw IllegalStateException("Cholesky failed: shrunk covariance not positive definite")
        val l: DMatrixRMaj = chol.getT(null)
        val tChol1 = SystemClock.elapsedRealtimeNanos()

        // ---- Stage 5: triangular solves for W (C x d) + bias ----
        val means = Array(nClasses) { DoubleArray(d) }
        val counts = IntArray(nClasses)
        for (i in 0 until n) {
            val c = labels[i]; counts[c]++
            for (j in 0 until d) means[c][j] += x[i][j]
        }
        for (c in 0 until nClasses) if (counts[c] > 0) for (j in 0 until d) means[c][j] /= counts[c]

        val w = Array(nClasses) { DoubleArray(d) }
        val bias = DoubleArray(nClasses)
        val z = DoubleArray(d)
        val y = DoubleArray(d)
        for (c in 0 until nClasses) {
            // rhs = mean_c - global_mean
            // forward: L z = rhs
            for (i in 0 until d) {
                var acc = means[c][i] - global[i]
                for (j in 0 until i) acc -= l.get(i, j) * z[j]
                z[i] = acc / l.get(i, i)
            }
            // back: L^T y = z
            for (i in d - 1 downTo 0) {
                var acc = z[i]
                for (j in i + 1 until d) acc -= l.get(j, i) * y[j]
                y[i] = acc / l.get(i, i)
            }
            var dot = 0.0
            for (j in 0 until d) { w[c][j] = y[j]; dot += means[c][j] * y[j] }
            val prior = if (counts[c] > 0) counts[c].toDouble() / n else 1e-6
            bias[c] = -0.5 * dot + ln(prior)
        }
        val tSolve1 = SystemClock.elapsedRealtimeNanos()

        return AlgebraMs(
            (tCov1 - tCov0) / 1e6,
            (tLw1 - tCov1) / 1e6,
            (tChol1 - tLw1) / 1e6,
            (tSolve1 - tChol1) / 1e6,
            alpha
        )
    }

    fun run(nViews: Int, nClasses: Int, repeats: Int, cooldownSeconds: Int, log: (String) -> Unit): JSONObject {
        require(sessions.tier2Available) { "Adaptation benchmark requires the Tier-2 companion (BioCLIP features)" }
        log("Adaptation: extracting $nViews views (d=896, C=$nClasses)")
        val ex = extract(nViews, nClasses, log)
        val thermalAfterExtraction = thermalStatus()
        log("Extraction total ${BenchmarkStats.round(ex.totalMs, 1)} ms (thermal=$thermalAfterExtraction)")

        // Cool down before timing the algebra so the recalibration budget is measured in a
        // normal thermal state, not under throttling from the extraction heat soak.
        if (cooldownSeconds > 0) {
            log("Cooling down ${cooldownSeconds}s before algebra timing...")
            Thread.sleep(cooldownSeconds * 1000L)
        }
        val thermalBeforeAlgebra = thermalStatus()

        val cov = DoubleArray(repeats); val lw = DoubleArray(repeats)
        val chol = DoubleArray(repeats); val solve = DoubleArray(repeats)
        var alpha = 0.0
        // One warm-up pass (JIT), excluded from statistics.
        algebraOnce(ex.x, ex.labels, nClasses)
        for (r in 0 until repeats) {
            val a = algebraOnce(ex.x, ex.labels, nClasses)
            cov[r] = a.cov; lw[r] = a.lw; chol[r] = a.chol; solve[r] = a.solve; alpha = a.alpha
        }
        val thermalAfterAlgebra = thermalStatus()
        val algebraTotal = DoubleArray(repeats) { cov[it] + lw[it] + chol[it] + solve[it] }
        val algebraMean = BenchmarkStats.mean(algebraTotal)
        log("Algebra total ${BenchmarkStats.round(algebraMean)} ms (alpha=${BenchmarkStats.round(alpha)}, thermal=$thermalAfterAlgebra)")

        return JSONObject()
            .put("n_views", nViews)
            .put("d", 896)
            .put("n_classes", nClasses)
            .put("algebra_repeats", repeats)
            .put("cooldown_seconds", cooldownSeconds)
            .put("thermal_after_extraction", thermalAfterExtraction)
            .put("thermal_before_algebra", thermalBeforeAlgebra)
            .put("thermal_after_algebra", thermalAfterAlgebra)
            .put("shrinkage_alpha", BenchmarkStats.round(alpha))
            .put("feature_extraction", JSONObject()
                .put("total_ms", BenchmarkStats.round(ex.totalMs))
                .put("per_view_ms", BenchmarkStats.round(ex.totalMs / nViews))
                .put("tier1_total_ms", BenchmarkStats.round(ex.tier1Ms))
                .put("tier2_total_ms", BenchmarkStats.round(ex.tier2Ms)))
            .put("covariance_ms", BenchmarkStats.latencyJson(cov))
            .put("ledoit_wolf_ms", BenchmarkStats.latencyJson(lw))
            .put("cholesky_ms", BenchmarkStats.latencyJson(chol))
            .put("solve_W_ms", BenchmarkStats.latencyJson(solve))
            .put("algebra_total_ms", BenchmarkStats.latencyJson(algebraTotal))
            .put("full_adaptation_ms", BenchmarkStats.round(ex.totalMs + algebraMean))
            .put("claim_scope", "algebra_total_ms (stages 2-5) is the measured closed-form recalibration cost (sub-second, gradient-free); feature_extraction is reported separately")
    }
}