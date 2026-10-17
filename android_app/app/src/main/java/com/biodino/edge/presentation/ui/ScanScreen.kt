package com.biodino.edge.presentation.ui

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.BitmapFactory
import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.CameraAlt
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.EnergySavingsLeaf
import androidx.compose.material.icons.filled.FlashOff
import androidx.compose.material.icons.filled.FlashOn
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.LocalFlorist
import androidx.compose.material.icons.filled.Pause
import androidx.compose.material.icons.filled.PhotoLibrary
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material.icons.filled.VolumeOff
import androidx.compose.material.icons.filled.VolumeUp
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary
import com.biodino.edge.presentation.viewmodel.ScanViewModel

@Composable
fun ScanScreen(
    viewModel: ScanViewModel
) {
    val state by viewModel.uiState.collectAsState()
    val context = LocalContext.current

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        viewModel.onPermissionResult(isGranted)
    }

    // Gallery Photo Picker
    val galleryLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            try {
                context.contentResolver.openInputStream(uri)?.use { stream ->
                    val bitmap = BitmapFactory.decodeStream(stream)
                    if (bitmap != null) {
                        viewModel.analyzeGalleryImage(bitmap)
                    }
                }
            } catch (_: Exception) {}
        }
    }

    LaunchedEffect(Unit) {
        val currentPermission = ContextCompat.checkSelfPermission(
            context,
            Manifest.permission.CAMERA
        ) == PackageManager.PERMISSION_GRANTED
        viewModel.onPermissionResult(currentPermission)
        if (!currentPermission) {
            permissionLauncher.launch(Manifest.permission.CAMERA)
        }
    }

    Box(
        modifier = Modifier
            .fillMaxSize()
            .background(ForestDark)
    ) {
        if (state.isCameraPermissionGranted) {
            // Camera or Gallery Static Image View
            if (state.galleryBitmap != null) {
                Box(modifier = Modifier.fillMaxSize()) {
                    Image(
                        bitmap = state.galleryBitmap!!.asImageBitmap(),
                        contentDescription = "Imported foliage image",
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )

                    // Exit Gallery Mode Button
                    Button(
                        onClick = { viewModel.clearGalleryImage() },
                        colors = ButtonDefaults.buttonColors(
                            containerColor = ForestSurfaceGlass,
                            contentColor = TextPrimary
                        ),
                        shape = RoundedCornerShape(20.dp),
                        modifier = Modifier
                            .align(Alignment.TopCenter)
                            .padding(top = 96.dp)
                            .border(1.dp, BorderHighlight, RoundedCornerShape(20.dp))
                    ) {
                        Icon(Icons.Default.Close, contentDescription = null, modifier = Modifier.size(16.dp))
                        Spacer(modifier = Modifier.width(6.dp))
                        Text("Return to Live Camera", fontSize = 12.sp)
                    }
                }
            } else {
                CameraPreview(
                    isTorchActive = state.isTorchActive,
                    onFrameAvailable = { bitmap ->
                        viewModel.analyzeFrame(bitmap)
                    }
                )

                // Viewfinder Reticle Overlay
                ReticleOverlay(
                    isScanningPaused = state.isScanningPaused,
                    isBlurred = state.isBlurred,
                    isEcoMode = state.isEcoMode,
                    smoothedConfidence = state.smoothedConfidence,
                    isConfidentlyLocked = state.isConfidentlyLocked
                )
            }

            // Top Status Bar & Quick Actions
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .statusBarsPadding()
                    .padding(horizontal = 14.dp, vertical = 8.dp)
                    .clip(RoundedCornerShape(20.dp))
                    .background(ForestSurfaceGlass)
                    .border(1.dp, BorderHighlight, RoundedCornerShape(20.dp))
                    .padding(horizontal = 12.dp, vertical = 6.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                Row(verticalAlignment = Alignment.CenterVertically) {
                    Box(
                        modifier = Modifier
                            .size(9.dp)
                            .clip(CircleShape)
                            .background(
                                when {
                                    state.galleryBitmap != null -> Color(0xFF00B0FF)
                                    state.isScanningPaused -> Color.Gray
                                    else -> EmeraldNeon
                                }
                            )
                    )
                    Spacer(modifier = Modifier.width(8.dp))
                    Column {
                        Text(
                            text = if (state.galleryBitmap != null) "Gallery Mode" else "BioDINO-Edge",
                            color = TextPrimary,
                            fontSize = 14.sp,
                            fontWeight = FontWeight.Bold
                        )
                        Text(
                            text = if (state.isEcoMode) "Eco 15 FPS" else "Real-Time AI",
                            color = TextSecondary,
                            fontSize = 10.sp
                        )
                    }
                }

                // Action Icons (Torch, Pause, Eco, TTS, Gallery, Atlas, History)
                Row(verticalAlignment = Alignment.CenterVertically) {
                    // Torch
                    IconButton(
                        onClick = { viewModel.toggleTorch() },
                        modifier = Modifier.size(34.dp)
                    ) {
                        Icon(
                            imageVector = if (state.isTorchActive) Icons.Default.FlashOn else Icons.Default.FlashOff,
                            contentDescription = "Torch",
                            tint = if (state.isTorchActive) EmeraldNeon else TextSecondary,
                            modifier = Modifier.size(18.dp)
                        )
                    }

                    // Eco Mode
                    IconButton(
                        onClick = { viewModel.toggleEcoMode() },
                        modifier = Modifier.size(34.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.EnergySavingsLeaf,
                            contentDescription = "Eco Mode",
                            tint = if (state.isEcoMode) EmeraldNeon else TextSecondary,
                            modifier = Modifier.size(18.dp)
                        )
                    }

                    // TTS Voice
                    IconButton(
                        onClick = { viewModel.toggleTts() },
                        modifier = Modifier.size(34.dp)
                    ) {
                        Icon(
                            imageVector = if (state.isTtsEnabled) Icons.Default.VolumeUp else Icons.Default.VolumeOff,
                            contentDescription = "TTS Voice",
                            tint = if (state.isTtsEnabled) EmeraldNeon else TextSecondary,
                            modifier = Modifier.size(18.dp)
                        )
                    }

                    // Gallery Picker
                    IconButton(
                        onClick = { galleryLauncher.launch("image/*") },
                        modifier = Modifier.size(34.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.PhotoLibrary,
                            contentDescription = "Pick Photo",
                            tint = TextSecondary,
                            modifier = Modifier.size(18.dp)
                        )
                    }

                    // Atlas Knowledgebase
                    IconButton(
                        onClick = { viewModel.openAtlas(true) },
                        modifier = Modifier.size(34.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.LocalFlorist,
                            contentDescription = "Atlas",
                            tint = TextSecondary,
                            modifier = Modifier.size(18.dp)
                        )
                    }

                    // History Log
                    IconButton(
                        onClick = { viewModel.openHistory(true) },
                        modifier = Modifier.size(34.dp)
                    ) {
                        Icon(
                            imageVector = Icons.Default.History,
                            contentDescription = "History",
                            tint = TextSecondary,
                            modifier = Modifier.size(18.dp)
                        )
                    }
                }
            }

            // Bottom Clinical Diagnostic Card
            DiagnosticCard(
                modifier = Modifier.align(Alignment.BottomCenter),
                latestDiagnosis = state.latestDiagnosis,
                smoothedConfidence = state.smoothedConfidence,
                averageLatencyMs = state.averageLatencyMs,
                isHardwareAccelerated = state.isHardwareAccelerated,
                onSpeakDiagnosis = { viewModel.speakCurrentDiagnosis() }
            )

        } else {
            // Permission Request Screen
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(32.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Icon(
                    imageVector = Icons.Default.CameraAlt,
                    contentDescription = null,
                    tint = EmeraldNeon,
                    modifier = Modifier.size(72.dp)
                )
                Spacer(modifier = Modifier.height(20.dp))
                Text(
                    text = "Camera Permission Required",
                    color = TextPrimary,
                    fontSize = 20.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = "BioDINO-Edge requires real-time camera access to scan foliage and detect plant pathologies on-device.",
                    color = TextSecondary,
                    fontSize = 14.sp,
                    lineHeight = 20.sp,
                    modifier = Modifier.padding(horizontal = 16.dp)
                )
                Spacer(modifier = Modifier.height(28.dp))
                Button(
                    onClick = { permissionLauncher.launch(Manifest.permission.CAMERA) },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = EmeraldNeon,
                        contentColor = ForestDark
                    ),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text(
                        text = "Grant Camera Permission",
                        fontWeight = FontWeight.Bold,
                        fontSize = 14.sp
                    )
                }
            }
        }

        // Modals
        if (state.isAtlasOpen) {
            AtlasDialog(onDismiss = { viewModel.openAtlas(false) })
        }

        if (state.isHistoryOpen) {
            HistoryDialog(
                historyItems = state.scanHistory,
                onClearHistory = { viewModel.clearHistory() },
                onDismiss = { viewModel.openHistory(false) }
            )
        }
    }
}
