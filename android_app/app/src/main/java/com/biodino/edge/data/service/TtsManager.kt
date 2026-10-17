package com.biodino.edge.data.service

import android.content.Context
import android.speech.tts.TextToSpeech
import java.util.Locale

/**
 * Manages native on-device Text-To-Speech for auditory field diagnostics.
 */
class TtsManager(context: Context) : TextToSpeech.OnInitListener {

    private var tts: TextToSpeech? = TextToSpeech(context.applicationContext, this)
    private var isReady = false
    private var lastSpokenText: String? = null
    private var lastSpokenTimestamp: Long = 0L

    override fun onInit(status: Int) {
        if (status == TextToSpeech.SUCCESS) {
            val result = tts?.setLanguage(Locale.US)
            if (result != TextToSpeech.LANG_MISSING_DATA && result != TextToSpeech.LANG_NOT_SUPPORTED) {
                isReady = true
                tts?.setSpeechRate(0.95f)
                tts?.setPitch(1.0f)
            }
        }
    }

    /**
     * Speaks diagnosis text, avoiding repetitive announcements within cooldown window.
     */
    fun speakDiagnosis(commonName: String, confidencePercent: Int, isHealthy: Boolean, force: Boolean = false) {
        val now = System.currentTimeMillis()
        val textToSpeak = if (isHealthy) {
            "Diagnosed as $commonName with $confidencePercent percent certainty. Foliage is healthy."
        } else {
            "Warning. $commonName detected with $confidencePercent percent certainty. Pathology action required."
        }

        if (!force && textToSpeak == lastSpokenText && (now - lastSpokenTimestamp) < 8000L) {
            return
        }

        if (isReady) {
            lastSpokenText = textToSpeak
            lastSpokenTimestamp = now
            tts?.speak(textToSpeak, TextToSpeech.QUEUE_FLUSH, null, "BioDinoDiagnosis")
        }
    }

    fun stop() {
        if (isReady) {
            tts?.stop()
        }
    }

    fun shutdown() {
        try {
            tts?.stop()
            tts?.shutdown()
            tts = null
        } catch (_: Exception) {}
    }
}
