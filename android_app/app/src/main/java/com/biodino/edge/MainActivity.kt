package com.biodino.edge

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.lifecycle.viewmodel.compose.viewModel
import com.biodino.edge.presentation.theme.BioDinoTheme
import com.biodino.edge.presentation.ui.ScanScreen
import com.biodino.edge.presentation.viewmodel.ScanViewModel

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            BioDinoTheme {
                val viewModel: ScanViewModel = viewModel()
                ScanScreen(viewModel = viewModel)
            }
        }
    }
}
