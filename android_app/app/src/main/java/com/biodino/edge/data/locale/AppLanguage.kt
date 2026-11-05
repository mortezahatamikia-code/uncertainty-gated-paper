package com.biodino.edge.data.locale

/**
 * Supported internationalization locales in BioDINO-Edge.
 * Extensible for English, French, German, and Persian (RTL).
 * Ordered by global usage with Persian as the final entry.
 */
enum class AppLanguage(
    val code: String,
    val displayName: String,
    val nativeName: String,
    val flagEmoji: String,
    val isRtl: Boolean
) {
    ENGLISH("en", "English", "English", "🌐", false),
    FRENCH("fr", "French", "Français", "🇫🇷", false),
    GERMAN("de", "German", "Deutsch", "🇩🇪", false),
    PERSIAN("fa", "Persian", "فارسی", "🇮🇷", true);

    companion object {
        fun fromCode(code: String): AppLanguage =
            entries.firstOrNull { it.code.equals(code, ignoreCase = true) } ?: ENGLISH
    }
}
