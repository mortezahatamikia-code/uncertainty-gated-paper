package com.biodino.edge.data.locale

object AppLanguage {
    fun str(isFarsi: Boolean, en: String, fa: String): String {
        return if (isFarsi) fa else en
    }
}
