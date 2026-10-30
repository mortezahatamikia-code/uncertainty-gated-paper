package com.biodino.edge.data.locale

/**
 * Supported internationalization locales in BioDINO-Edge.
 * Extensible for English, Persian (RTL), German, and French.
 */
enum class AppLanguage(
    val code: String,
    val displayName: String,
    val nativeName: String,
    val flagEmoji: String,
    val isRtl: Boolean
) {
    ENGLISH("en", "English", "English", "🌐", false),
    PERSIAN("fa", "Persian", "فارسی", "🇮🇷", true),
    GERMAN("de", "German", "Deutsch", "🇩🇪", false),
    FRENCH("fr", "French", "Français", "🇫🇷", false);

    companion object {
        fun fromCode(code: String): AppLanguage =
            entries.firstOrNull { it.code.equals(code, ignoreCase = true) } ?: ENGLISH
    }
}
