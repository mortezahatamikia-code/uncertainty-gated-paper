package com.biodino.edge.presentation.theme

import android.app.Activity
import androidx.compose.foundation.isSystemInDarkTheme
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.runtime.SideEffect
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.platform.LocalView
import androidx.core.view.WindowCompat

private val DarkColorScheme = darkColorScheme(
    primary = EmeraldNeon,
    onPrimary = ForestDark,
    primaryContainer = ForestSurface,
    onPrimaryContainer = EmeraldNeon,
    secondary = EmeraldAccent,
    onSecondary = ForestDark,
    background = ForestDark,
    onBackground = TextPrimary,
    surface = ForestSurface,
    onSurface = TextPrimary,
    surfaceVariant = ForestSurfaceGlass,
    onSurfaceVariant = TextSecondary,
    error = AlertCrimson,
    onError = TextPrimary
)

@Composable
fun BioDinoTheme(
    content: @Composable () -> Unit
) {
    val view = LocalView.current
    if (!view.isInEditMode) {
        SideEffect {
            val window = (view.context as Activity).window
            window.statusBarColor = ForestDark.toArgb()
            window.navigationBarColor = ForestDark.toArgb()
            WindowCompat.getInsetsController(window, view).isAppearanceLightStatusBars = false
            WindowCompat.getInsetsController(window, view).isAppearanceLightNavigationBars = false
        }
    }

    MaterialTheme(
        colorScheme = DarkColorScheme,
        typography = Typography,
        content = content
    )
}
