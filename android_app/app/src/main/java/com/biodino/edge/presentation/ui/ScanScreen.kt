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
import androidx.compose.material.icons.filled.Warning
import com.biodino.edge.data.engine.BitmapUtils
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.AlertCrimson
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurface
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

    // Photo Gallery Picker (Robust Software Decoding & EXIF orientation support)
    val galleryLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            try {
                val bitmap = BitmapUtils.decodeSoftwareBitmap(context, uri)
                if (bitmap != null) {
                    viewModel.analyzeGalleryImage(bitmap)
                } else {
                    viewModel.onGalleryError(
                        if (isFarsi) "قالب تصویر قابل پردازش نیست یا حجم تصویر بسیار بالاست." else "Unable to decode foliage image from storage."
                    )
                }
            } catch (t: Throwable) {
                viewModel.onGalleryError(
                    if (isFarsi) "خطا در خواندن فایل از حافظه: ${t.localizedMessage}" else "Failed to load image: ${t.localizedMessage}"
                )
            }
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
                    isFarsi = isFarsi,
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

            // Error Notification Pill if any operation fails
            if (state.errorMessage != null) {
                Box(
                    modifier = Modifier
                        .align(Alignment.TopCenter)
                        .statusBarsPadding()
                        .padding(top = 64.dp, start = 16.dp, end = 16.dp)
                        .clip(RoundedCornerShape(16.dp))
                        .background(AlertCrimson.copy(alpha = 0.95f))
                        .border(1.dp, Color.White.copy(alpha = 0.35f), RoundedCornerShape(16.dp))
                        .padding(horizontal = 14.dp, vertical = 8.dp)
                ) {
                    Row(
                        verticalAlignment = Alignment.CenterVertically,
                        horizontalArrangement = Arrangement.SpaceBetween,
                        modifier = Modifier.fillMaxWidth()
                    ) {
                        Row(
                            verticalAlignment = Alignment.CenterVertically,
                            modifier = Modifier.weight(1f)
                        ) {
                            Icon(Icons.Default.Warning, contentDescription = null, tint = Color.White, modifier = Modifier.size(18.dp))
                            Spacer(modifier = Modifier.width(8.dp))
                            Text(
                                text = state.errorMessage!!,
                                color = Color.White,
                                fontSize = 12.sp,
                                fontWeight = FontWeight.Bold
                            )
                        }
                        IconButton(
                            onClick = { viewModel.clearErrorMessage() },
                            modifier = Modifier.size(24.dp)
                        ) {
                            Icon(Icons.Default.Close, contentDescription = "Dismiss", tint = Color.White, modifier = Modifier.size(16.dp))
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
                    // 1. Live Diagnosis / Scan Mode (DEFAULT & PRIMARY ACTIVE TAB)
                    val isLiveMode = state.galleryBitmap == null
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(if (isLiveMode) EmeraldNeon.copy(alpha = 0.22f) else ForestSurface)
                            .border(1.dp, if (isLiveMode) EmeraldNeon else BorderHighlight, RoundedCornerShape(16.dp))
                            .clickable { viewModel.clearGalleryImage() }
                            .padding(horizontal = 12.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                Icons.Default.CameraAlt,
                                contentDescription = null,
                                tint = if (isLiveMode) EmeraldNeon else TextSecondary,
                                modifier = Modifier.size(17.dp)
                            )
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(
                                text = if (isFarsi) "تشخیص زنده" else "Live Scan",
                                color = if (isLiveMode) EmeraldNeon else TextPrimary,
                                fontSize = 11.sp,
                                fontWeight = if (isLiveMode) FontWeight.Bold else FontWeight.Medium
                            )
                        }
                    }

                    // 2. Gallery Picker
                    val isGalleryMode = state.galleryBitmap != null
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(if (isGalleryMode) Color(0xFF00B0FF).copy(alpha = 0.22f) else ForestSurface)
                            .border(1.dp, if (isGalleryMode) Color(0xFF00B0FF) else BorderHighlight, RoundedCornerShape(16.dp))
                            .clickable { galleryLauncher.launch("image/*") }
                            .padding(horizontal = 11.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(
                                Icons.Default.PhotoLibrary,
                                contentDescription = null,
                                tint = if (isGalleryMode) Color(0xFF00B0FF) else TextPrimary,
                                modifier = Modifier.size(17.dp)
                            )
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(
                                text = if (isFarsi) "گالری" else "Gallery",
                                color = if (isGalleryMode) Color(0xFF00B0FF) else TextPrimary,
                                fontSize = 11.sp,
                                fontWeight = if (isGalleryMode) FontWeight.Bold else FontWeight.SemiBold
                            )
                        }
                    }

                    // 3. Atlas
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(ForestSurface)
                            .border(1.dp, BorderHighlight, RoundedCornerShape(16.dp))
                            .clickable { viewModel.openAtlas(true) }
                            .padding(horizontal = 10.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.LocalFlorist, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(if (isFarsi) "اطلس" else "Atlas", color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }

                    // 4. Dosage Calculator
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(ForestSurface)
                            .border(1.dp, BorderHighlight, RoundedCornerShape(16.dp))
                            .clickable { viewModel.openCalculator(true) }
                            .padding(horizontal = 10.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.Calculate, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(if (isFarsi) "محاسبه دوز" else "Dosage", color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }

                    // 5. Weather Spray Window
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(ForestSurface)
                            .border(1.dp, BorderHighlight, RoundedCornerShape(16.dp))
                            .clickable { viewModel.openWeather(true) }
                            .padding(horizontal = 10.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.WbSunny, contentDescription = null, tint = AlertAmber, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(if (isFarsi) "هواشناسی سم" else "Weather", color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }

                    // 6. History
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(ForestSurface)
                            .border(1.dp, BorderHighlight, RoundedCornerShape(16.dp))
                            .clickable { viewModel.openHistory(true) }
                            .padding(horizontal = 10.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.History, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(if (isFarsi) "تاریخچه" else "History", color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
                        }
                    }

                    // 7. Few-Shot Class Enrollment (Custom Calibration)
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(ForestSurface)
                            .border(1.dp, BorderHighlight, RoundedCornerShape(16.dp))
                            .clickable { viewModel.openEnrollment(true) }
                            .padding(horizontal = 11.dp, vertical = 7.dp)
                    ) {
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Icon(Icons.Default.AddCircle, contentDescription = null, tint = EmeraldAccent, modifier = Modifier.size(17.dp))
                            Spacer(modifier = Modifier.width(5.dp))
                            Text(
                                text = if (isFarsi) "+ افزودن بیماری جدید (۵-شات)" else "+ Enroll Class (5-Shot)",
                                color = EmeraldAccent,
                                fontSize = 11.sp,
                                fontWeight = FontWeight.Medium
                            )
                        }
                    }

                    // 8. Eco Mode
                    Box(
                        modifier = Modifier
                            .clip(RoundedCornerShape(16.dp))
                            .background(if (state.isEcoMode) EmeraldNeon.copy(alpha = 0.2f) else ForestSurface)
                            .border(1.dp, if (state.isEcoMode) EmeraldNeon else BorderHighlight, RoundedCornerShape(16.dp))
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
                    isGalleryMode = state.galleryBitmap != null,
                    isTooDark = state.isTooDark,
                    isNonLeaf = state.isNonLeaf,
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
            AtlasSheet(
                isFarsi = isFarsi,
                onDismiss = { viewModel.openAtlas(false) }
            )
        }

        if (state.isHistoryOpen) {
            HistorySheet(
                isFarsi = isFarsi,
                historyItems = state.scanHistory,
                onClearHistory = { viewModel.clearHistory() },
                onDismiss = { viewModel.openHistory(false) }
            )
        }
    }
}
