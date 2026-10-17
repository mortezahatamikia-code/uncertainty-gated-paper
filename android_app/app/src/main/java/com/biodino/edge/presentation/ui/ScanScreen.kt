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
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
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
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.VolumeOff
import androidx.compose.material.icons.automirrored.filled.VolumeUp
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material.icons.filled.Calculate
import androidx.compose.material.icons.filled.CameraAlt
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.EnergySavingsLeaf
import androidx.compose.material.icons.filled.FlashOff
import androidx.compose.material.icons.filled.FlashOn
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.Language
import androidx.compose.material.icons.filled.LocalFlorist
import androidx.compose.material.icons.filled.PhotoLibrary
import androidx.compose.material.icons.filled.WbSunny
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
    val isFarsi = state.isFarsi

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        viewModel.onPermissionResult(isGranted)
    }

    // Photo Gallery Picker
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
            // Camera Stream OR Gallery Inspection View
            if (state.galleryBitmap != null) {
                Box(modifier = Modifier.fillMaxSize()) {
                    Image(
                        bitmap = state.galleryBitmap!!.asImageBitmap(),
                        contentDescription = "Imported foliage",
                        modifier = Modifier.fillMaxSize(),
                        contentScale = ContentScale.Crop
                    )

                    // Return to Live Camera Pill
                    Box(
                        modifier = Modifier
                            .align(Alignment.TopCenter)
                            .statusBarsPadding()
                            .padding(top = 70.dp)
                            .clip(RoundedCornerShape(20.dp))
                            .background(ForestSurfaceGlass)
                            .border(1.dp, EmeraldNeon, RoundedCornerShape(20.dp))
                            .clickable { viewModel.clearGalleryImage() }
                            .padding(horizontal = 16.dp, vertical = 8.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Close, contentDescription = null, tint = EmeraldNeon, modifier = Modifier.size(16.dp))
                            Spacer(modifier = Modifier.width(6.dp))
                            Text(
                                text = if (isFarsi) "حالت بازبینی گالری • لمس برای بازگشت به دوربین زنده" else "Gallery View • Tap to return to Live Camera",
                                color = TextPrimary,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }
                }
            } else {
                CameraPreview(
                    isTorchActive = state.isTorchActive,
                    onFrameAvailable = { bitmap ->
                        viewModel.analyzeFrame(bitmap)
                    }
                )

                // High-Tech Organic Reticle
                ReticleOverlay(
                    isScanningPaused = state.isScanningPaused,
                    isBlurred = state.isBlurred,
                    isEcoMode = state.isEcoMode,
                    smoothedConfidence = state.smoothedConfidence,
                    isConfidentlyLocked = state.isConfidentlyLocked
                )
            }

            // Top Bar: Clean Minimalist Brand, Language Toggle & Controls
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .statusBarsPadding()
                    .padding(horizontal = 16.dp, vertical = 10.dp),
                horizontalArrangement = Arrangement.SpaceBetween,
                verticalAlignment = Alignment.CenterVertically
            ) {
                // Brand Logo & Live Beacon
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(20.dp))
                        .background(ForestSurfaceGlass)
                        .border(1.dp, BorderHighlight, RoundedCornerShape(20.dp))
                        .padding(horizontal = 14.dp, vertical = 8.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Box(
                            modifier = Modifier
                                .size(9.dp)
                                .clip(CircleShape)
                                .background(if (state.galleryBitmap != null) Color(0xFF00B0FF) else EmeraldNeon)
                        )
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(
                            text = "BioDINO",
                            color = TextPrimary,
                            fontSize = 15.sp,
                            fontWeight = FontWeight.Bold,
                            letterSpacing = 0.5.sp
                        )
                        Spacer(modifier = Modifier.width(4.dp))
                        Text(
                            text = "EDGE",
                            color = EmeraldNeon,
                            fontSize = 10.sp,
                            fontWeight = FontWeight.Bold
                        )
                    }
                }

                // Floating Glass Capsule: Language Toggle, Torch, Audio
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(20.dp))
                        .background(ForestSurfaceGlass)
                        .border(1.dp, BorderHighlight, RoundedCornerShape(20.dp))
                        .padding(horizontal = 4.dp, vertical = 2.dp)
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        // FA / EN Switch
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(12.dp))
                                .clickable { viewModel.toggleFarsi() }
                                .padding(horizontal = 8.dp, vertical = 6.dp)
                        ) {
                            Text(
                                text = if (isFarsi) "FA 🇮🇷" else "EN 🌐",
                                color = if (isFarsi) EmeraldNeon else TextPrimary,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }

                        Box(modifier = Modifier.width(1.dp).height(18.dp).background(BorderHighlight))

                        // Torch Button
                        IconButton(
                            onClick = { viewModel.toggleTorch() },
                            modifier = Modifier.size(36.dp)
                        ) {
                            Icon(
                                imageVector = if (state.isTorchActive) Icons.Default.FlashOn else Icons.Default.FlashOff,
                                contentDescription = "Torch",
                                tint = if (state.isTorchActive) EmeraldNeon else TextSecondary,
                                modifier = Modifier.size(19.dp)
                            )
                        }

                        Box(modifier = Modifier.width(1.dp).height(18.dp).background(BorderHighlight))

                        // TTS Audio Button
                        IconButton(
                            onClick = { viewModel.toggleTts() },
                            modifier = Modifier.size(36.dp)
                        ) {
                            Icon(
                                imageVector = if (state.isTtsEnabled) Icons.AutoMirrored.Filled.VolumeUp else Icons.AutoMirrored.Filled.VolumeOff,
                                contentDescription = "TTS",
                                tint = if (state.isTtsEnabled) EmeraldNeon else TextSecondary,
                                modifier = Modifier.size(19.dp)
                            )
                        }
                    }
                }
            }

            // Bottom Stack: Floating Action Dock + Diagnostic Card
            Column(
                modifier = Modifier
                    .align(Alignment.BottomCenter)
                    .fillMaxWidth()
            ) {
                // Floating Action Tool Dock (Scrollable thumb-friendly dock)
                val dockScrollState = rememberScrollState()
                Row(
                    modifier = Modifier
                        .align(Alignment.CenterHorizontally)
                        .padding(horizontal = 14.dp)
                        .padding(bottom = 10.dp)
                        .clip(RoundedCornerShape(24.dp))
                        .background(ForestSurfaceGlass)
                        .border(1.dp, BorderHighlight, RoundedCornerShape(24.dp))
                        .horizontalScroll(dockScrollState)
                        .padding(horizontal = 8.dp, vertical = 4.dp),
                    horizontalArrangement = Arrangement.spacedBy(6.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    // 1. Few-Shot Class Enrollment (New Crop / Disease)
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(EmeraldNeon.copy(alpha = 0.18f))
                            .border(1.dp, EmeraldNeon, RoundedCornerShape(16.dp))
                            .clickable { viewModel.openEnrollment(true) }
                            .padding(horizontal = 12.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.AddCircle, contentDescription = null, tint = EmeraldNeon, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(
                                text = if (isFarsi) "+ تعریف بیماری جدید (۵ شات)" else "+ Enroll Class (5-Shot)",
                                color = EmeraldNeon,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                    }

                    // 2. Dosage Calculator
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .clickable { viewModel.openCalculator(true) }
                            .padding(horizontal = 10.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Calculate, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(if (isFarsi) "محاسبه دوز" else "Dosage", color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }

                    // 3. Weather Spray Window
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .clickable { viewModel.openWeather(true) }
                            .padding(horizontal = 10.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.WbSunny, contentDescription = null, tint = AlertAmber, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(if (isFarsi) "هواشناسی سم" else "Weather", color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }

                    // 4. Atlas
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .clickable { viewModel.openAtlas(true) }
                            .padding(horizontal = 10.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.LocalFlorist, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(if (isFarsi) "اطلس" else "Atlas", color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }

                    // 5. History
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .clickable { viewModel.openHistory(true) }
                            .padding(horizontal = 10.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.History, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(if (isFarsi) "تاریخچه" else "History", color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }

                    // 6. Gallery Picker
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .clickable { galleryLauncher.launch("image/*") }
                            .padding(horizontal = 10.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.PhotoLibrary, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(if (isFarsi) "گالری" else "Gallery", color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }

                    // 7. Eco Mode
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(if (state.isEcoMode) EmeraldNeon.copy(alpha = 0.2f) else Color.Transparent)
                            .clickable { viewModel.toggleEcoMode() }
                            .padding(horizontal = 8.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                Icons.Default.EnergySavingsLeaf,
                                contentDescription = null,
                                tint = if (state.isEcoMode) EmeraldNeon else TextSecondary,
                                modifier = Modifier.size(17.dp)
                            )
                            if (state.isEcoMode) {
                                Spacer(modifier = Modifier.width(4.dp))
                                Text("ECO", color = EmeraldNeon, fontSize = 10.sp, fontWeight = FontWeight.Bold)
                            }
                        }
                    }
                }

                // Progressive Disclosure Diagnostic Card
                DiagnosticCard(
                    isFarsi = isFarsi,
                    latestDiagnosis = state.latestDiagnosis,
                    smoothedConfidence = state.smoothedConfidence,
                    averageLatencyMs = state.averageLatencyMs,
                    isHardwareAccelerated = state.isHardwareAccelerated,
                    onSpeakDiagnosis = { viewModel.speakCurrentDiagnosis() },
                    onOpenCalculator = { viewModel.openCalculator(true) }
                )
            }

        } else {
            // Camera Permission Request Screen
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(32.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Box(
                    modifier = Modifier
                        .size(96.dp)
                        .clip(CircleShape)
                        .background(EmeraldNeon.copy(alpha = 0.15f)),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = Icons.Default.CameraAlt,
                        contentDescription = null,
                        tint = EmeraldNeon,
                        modifier = Modifier.size(48.dp)
                    )
                }
                Spacer(modifier = Modifier.height(24.dp))
                Text(
                    text = if (isFarsi) "مجوز دسترسی به دوربین الزامی است" else "Camera Permission Required",
                    color = TextPrimary,
                    fontSize = 21.sp,
                    fontWeight = FontWeight.Bold
                )
                Spacer(modifier = Modifier.height(8.dp))
                Text(
                    text = if (isFarsi) "سامانه BioDINO-Edge برای اسکن برگ‌ها و تشخیص زنده بیماری‌های گیاهی به دسترسی دوربین نیاز دارد." else "BioDINO-Edge runs real-time plant pathology vision on your device. Camera access is needed to scan foliage.",
                    color = TextSecondary,
                    fontSize = 14.sp,
                    lineHeight = 20.sp,
                    modifier = Modifier.padding(horizontal = 12.dp)
                )
                Spacer(modifier = Modifier.height(28.dp))
                Button(
                    onClick = { permissionLauncher.launch(Manifest.permission.CAMERA) },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = EmeraldNeon,
                        contentColor = ForestDark
                    ),
                    shape = RoundedCornerShape(14.dp),
                    modifier = Modifier.height(48.dp)
                ) {
                    Text(
                        text = if (isFarsi) "تایید و فعال‌سازی دوربین" else "Enable Camera Access",
                        fontWeight = FontWeight.Bold,
                        fontSize = 14.sp
                    )
                }
            }
        }

        // Modals & Bottom Sheets
        if (state.isEnrollmentOpen) {
            FewShotEnrollmentSheet(
                customClasses = state.customEnrolledDiseases,
                onEnroll = { name, host, latin, healthy, advice, photos ->
                    viewModel.enrollCustomClass(name, host, latin, healthy, advice, photos)
                },
                onDeleteClass = { id -> viewModel.deleteCustomDisease(id) },
                onDismiss = { viewModel.openEnrollment(false) }
            )
        }

        if (state.isCalculatorOpen) {
            DosageCalculatorSheet(
                isFarsi = isFarsi,
                onDismiss = { viewModel.openCalculator(false) }
            )
        }

        if (state.isWeatherOpen) {
            WeatherWindowSheet(
                isFarsi = isFarsi,
                onDismiss = { viewModel.openWeather(false) }
            )
        }

        if (state.isAtlasOpen) {
            AtlasSheet(onDismiss = { viewModel.openAtlas(false) })
        }

        if (state.isHistoryOpen) {
            HistorySheet(
                historyItems = state.scanHistory,
                onClearHistory = { viewModel.clearHistory() },
                onDismiss = { viewModel.openHistory(false) }
            )
        }
    }
}
