package com.biodino.edge.presentation.scan

import android.Manifest
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.statusBarsPadding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Close
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.core.content.ContextCompat
import com.biodino.edge.data.image.BitmapUtils
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.I18n
import com.biodino.edge.data.locale.LocalAppLanguage
import com.biodino.edge.data.locale.LocalAppStrings
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.viewmodel.ScanViewModel
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

@Composable
fun ScanScreen(
    viewModel: ScanViewModel
) {
    val state by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val coroutineScope = rememberCoroutineScope()
    val language = state.currentLanguage
    val strings = I18n.getStrings(language)
    val isFarsi = language == AppLanguage.PERSIAN
    val layoutDirection = if (language.isRtl) LayoutDirection.Rtl else LayoutDirection.Ltr

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { isGranted ->
        viewModel.onPermissionResult(isGranted)
    }

    // Gallery picker
    val galleryLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetContent()
    ) { uri: Uri? ->
        if (uri != null) {
            coroutineScope.launch(Dispatchers.IO) {
                try {
                    val bitmap = BitmapUtils.decodeSoftwareBitmap(context, uri)
                    withContext(Dispatchers.Main) {
                        if (bitmap != null) {
                            viewModel.analyzeGalleryImage(bitmap)
                        } else {
                            viewModel.onGalleryError(strings.errorUnableToDecodeGallery)
                        }
                    }
                } catch (t: Throwable) {
                    withContext(Dispatchers.Main) {
                        viewModel.onGalleryError(strings.errorLoadingGallery(t.localizedMessage ?: ""))
                    }
                }
            }
        }
    }

    val galleryPermission = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        Manifest.permission.READ_MEDIA_IMAGES
    } else {
        Manifest.permission.READ_EXTERNAL_STORAGE
    }

    val galleryPermissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { _ ->
        galleryLauncher.launch("image/*")
    }

    fun launchGalleryWithPermissionCheck() {
        if (ContextCompat.checkSelfPermission(context, galleryPermission) == PackageManager.PERMISSION_GRANTED) {
            galleryLauncher.launch("image/*")
        } else {
            galleryPermissionLauncher.launch(galleryPermission)
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

    CompositionLocalProvider(
        LocalLayoutDirection provides layoutDirection,
        LocalAppLanguage provides language,
        LocalAppStrings provides strings
    ) {
        Box(
            modifier = Modifier
                .fillMaxSize()
                .background(ForestDark)
        ) {
            if (state.isCameraPermissionGranted) {
                if (state.galleryBitmap != null) {
                    Column(
                        modifier = Modifier
                            .fillMaxWidth()
                            .fillMaxHeight(0.50f)
                            .align(Alignment.TopCenter)
                            .padding(bottom = 8.dp),
                        horizontalAlignment = Alignment.CenterHorizontally
                    ) {
                        // Spacing below the status bar and TopBar
                        Spacer(
                            modifier = Modifier
                                .statusBarsPadding()
                                .height(56.dp)
                        )

                        // Back to camera pill
                        Box(
                            modifier = Modifier
                                .clip(RoundedCornerShape(20.dp))
                                .background(ForestSurfaceGlass)
                                .border(1.dp, EmeraldNeon, RoundedCornerShape(20.dp))
                                .clickable { viewModel.clearGalleryImage() }
                                .padding(horizontal = 14.dp, vertical = 6.dp)
                        ) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(
                                    Icons.Default.Close,
                                    contentDescription = null,
                                    tint = EmeraldNeon,
                                    modifier = Modifier.size(14.dp)
                                )
                                Spacer(modifier = Modifier.width(6.dp))
                                Text(
                                    text = strings.galleryModeReturnHint,
                                    color = TextPrimary,
                                    fontSize = 11.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }
                        }

                        Spacer(modifier = Modifier.height(8.dp))

                        // Leaf photo rendered strictly within top 50% of the screen
                        Image(
                            bitmap = state.galleryBitmap!!.asImageBitmap(),
                            contentDescription = "Imported foliage",
                            modifier = Modifier
                                .fillMaxWidth()
                                .weight(1f)
                                .padding(horizontal = 12.dp),
                            contentScale = ContentScale.Fit,
                            alignment = Alignment.Center
                        )
                    }
                } else {
                    if (state.isCameraActive) {
                        CameraPreview(
                            isTorchActive = state.isTorchActive,
                            onFrameAvailable = { bitmap ->
                                viewModel.analyzeFrame(bitmap)
                            }
                        )

                        // Viewfinder overlay
                        ReticleOverlay(
                            language = language,
                            isFarsi = isFarsi,
                            isScanningPaused = state.isScanningPaused,
                            isBlurred = state.isBlurred,
                            isEcoMode = state.isEcoMode,
                            smoothedConfidence = state.smoothedConfidence,
                            isConfidentlyLocked = state.isConfidentlyLocked
                        )
                    } else {
                        CameraStandbyView(
                            language = language,
                            onResumeCamera = { viewModel.toggleCameraActive(true) }
                        )
                    }
                }

                // Top bar
                ScanTopBar(
                    language = language,
                    isTorchActive = state.isTorchActive,
                    isTtsEnabled = state.isTtsEnabled,
                    onLanguageClick = { viewModel.showLanguageDialog(true) },
                    onTorchToggle = { viewModel.toggleTorch() },
                    onTtsToggle = { viewModel.toggleTts() }
                )

                // Notifications
                ScanToastHost(
                    errorMessage = state.errorMessage,
                    successMessage = state.successMessage,
                    onClearError = { viewModel.clearErrorMessage() },
                    onClearSuccess = { viewModel.clearSuccessMessage() }
                )

                // Bottom controls & diagnosis
                ScanBottomBar(
                    language = language,
                    strings = strings,
                    isFarsi = isFarsi,
                    isCameraActive = state.isCameraActive,
                    isGalleryMode = state.galleryBitmap != null,
                    isUsingCustomModel = state.isUsingCustomModel,
                    isEcoMode = state.isEcoMode,
                    isTooDark = state.isTooDark,
                    isNonLeaf = state.isNonLeaf,
                    latestDiagnosis = state.latestDiagnosis,
                    smoothedConfidence = state.smoothedConfidence,
                    averageLatencyMs = state.averageLatencyMs,
                    isHardwareAccelerated = state.isHardwareAccelerated,
                    onToggleCameraActive = { active -> viewModel.toggleCameraActive(active) },
                    onClearGalleryImage = { viewModel.clearGalleryImage() },
                    onLaunchGallery = { launchGalleryWithPermissionCheck() },
                    onOpenAtlas = { viewModel.openAtlas(true) },
                    onOpenCalculator = { viewModel.openCalculator(true) },
                    onOpenHistory = { viewModel.openHistory(true) },
                    onOpenEnrollment = { viewModel.openEnrollment(true) },
                    onOpenModelManager = { viewModel.openModelManager(true) },
                    onToggleEcoMode = { viewModel.toggleEcoMode() },
                    onSpeakDiagnosis = { viewModel.speakCurrentDiagnosis() },
                    onOpenCareGuide = { viewModel.openCareGuide(true) },
                    modifier = Modifier.align(Alignment.BottomCenter)
                )

            } else {
                CameraPermissionView(
                    strings = strings,
                    onRequestPermission = { permissionLauncher.launch(Manifest.permission.CAMERA) }
                )
            }

            // Modals & Bottom Sheets Host
            ScanSheetsHost(
                state = state,
                language = language,
                strings = strings,
                isFarsi = isFarsi,
                viewModel = viewModel
            )
        }
    }
}
