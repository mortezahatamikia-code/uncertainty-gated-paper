package com.biodino.edge.presentation.enrollment

import android.Manifest
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.net.Uri
import android.os.Build
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.core.content.ContextCompat
import com.biodino.edge.data.image.BitmapUtils
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AddPhotoAlternate
import androidx.compose.material.icons.filled.Check
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Delete
import androidx.compose.material.icons.filled.Psychology
import androidx.compose.material.icons.filled.RocketLaunch
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Card
import androidx.compose.material3.CardDefaults
import androidx.compose.material3.CircularProgressIndicator
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.OutlinedTextFieldDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.CompositionLocalProvider
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateListOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.asImageBitmap
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.LocalLayoutDirection
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.LayoutDirection
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.window.Dialog
import com.biodino.edge.data.locale.AppLanguage
import com.biodino.edge.data.locale.I18n
import com.biodino.edge.domain.model.CustomEnrolledDisease
import com.biodino.edge.presentation.theme.AlertAmber
import com.biodino.edge.presentation.theme.AlertCrimson
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary
import com.biodino.edge.presentation.common.SheetCloseButton
import com.biodino.edge.presentation.common.SheetDragHandle

@Composable
fun FewShotEnrollmentSheet(
    isFarsi: Boolean = false,
    language: AppLanguage = if (isFarsi) AppLanguage.PERSIAN else AppLanguage.ENGLISH,
    customClasses: List<CustomEnrolledDisease>,
    onEnroll: (name: String, host: String, latin: String, isHealthy: Boolean, advice: String, photos: List<Bitmap>, healthyPhotos: List<Bitmap>) -> Unit,
    onDeleteClass: (String) -> Unit,
    onDismiss: () -> Unit
) {
    val context = LocalContext.current
    val strings = I18n.getStrings(language)
    var diseaseName by remember { mutableStateOf("") }
    var hostPlant by remember { mutableStateOf("") }
    var adviceText by remember { mutableStateOf("") }
    var isCalibrating by remember { mutableStateOf(false) }

    val capturedPhotos = remember { mutableStateListOf<Bitmap>() }
    val healthyPhotos = remember { mutableStateListOf<Bitmap>() }
    val coroutineScope = rememberCoroutineScope()

    val galleryPermission = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
        Manifest.permission.READ_MEDIA_IMAGES
    } else {
        Manifest.permission.READ_EXTERNAL_STORAGE
    }

    var pendingPickerTarget by remember { mutableStateOf<String?>(null) }

    val galleryLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetMultipleContents()
    ) { uris: List<Uri> ->
        coroutineScope.launch(Dispatchers.IO) {
            val remaining = 5 - capturedPhotos.size
            for (uri in uris.take(remaining)) {
                try {
                    val bmp = BitmapUtils.decodeSoftwareBitmap(context, uri, maxDimension = 640)
                    if (bmp != null) {
                        val square = BitmapUtils.centerCropToSquare(bmp)
                        withContext(Dispatchers.Main) {
                            capturedPhotos.add(square)
                        }
                    }
                } catch (_: Exception) {}
            }
        }
    }

    val healthyGalleryLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.GetMultipleContents()
    ) { uris: List<Uri> ->
        coroutineScope.launch(Dispatchers.IO) {
            val remaining = 5 - healthyPhotos.size
            for (uri in uris.take(remaining)) {
                try {
                    val bmp = BitmapUtils.decodeSoftwareBitmap(context, uri, maxDimension = 640)
                    if (bmp != null) {
                        val square = BitmapUtils.centerCropToSquare(bmp)
                        withContext(Dispatchers.Main) {
                            healthyPhotos.add(square)
                        }
                    }
                } catch (_: Exception) {}
            }
        }
    }

    val permissionLauncher = rememberLauncherForActivityResult(
        contract = ActivityResultContracts.RequestPermission()
    ) { _ ->
        if (pendingPickerTarget == "healthy") {
            healthyGalleryLauncher.launch("image/*")
        } else {
            galleryLauncher.launch("image/*")
        }
    }

    fun launchDiseasedGallery() {
        if (ContextCompat.checkSelfPermission(context, galleryPermission) == PackageManager.PERMISSION_GRANTED) {
            galleryLauncher.launch("image/*")
        } else {
            pendingPickerTarget = "diseased"
            permissionLauncher.launch(galleryPermission)
        }
    }

    fun launchHealthyGallery() {
        if (ContextCompat.checkSelfPermission(context, galleryPermission) == PackageManager.PERMISSION_GRANTED) {
            healthyGalleryLauncher.launch("image/*")
        } else {
            pendingPickerTarget = "healthy"
            permissionLauncher.launch(galleryPermission)
        }
    }

    Dialog(onDismissRequest = onDismiss) {
        CompositionLocalProvider(
            LocalLayoutDirection provides (if (language.isRtl) LayoutDirection.Rtl else LayoutDirection.Ltr)
        ) {
            Box(
                modifier = Modifier
                    .fillMaxWidth()
                    .fillMaxHeight(0.92f)
                    .clip(RoundedCornerShape(28.dp))
                    .background(ForestDark)
                    .border(1.dp, BorderHighlight, RoundedCornerShape(28.dp))
                    .padding(20.dp)
            ) {
                Column(modifier = Modifier.fillMaxWidth()) {
                    // Drag Handle
                    SheetDragHandle(modifier = Modifier.align(Alignment.CenterHorizontally))

                    Spacer(modifier = Modifier.height(14.dp))

                    // Header
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.CenterVertically
                    ) {
                        Row(
                            modifier = Modifier.weight(1f),
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            Box(
                                modifier = Modifier
                                    .size(36.dp)
                                    .clip(CircleShape)
                                    .background(EmeraldNeon.copy(alpha = 0.15f)),
                                contentAlignment = Alignment.Center
                            ) {
                                Icon(
                                    imageVector = Icons.Default.Psychology,
                                    contentDescription = null,
                                    tint = EmeraldNeon,
                                    modifier = Modifier.size(22.dp)
                                )
                            }
                            Spacer(modifier = Modifier.width(10.dp))
                            Column(modifier = Modifier.padding(end = 8.dp)) {
                                Text(
                                    text = strings.enrollTitle,
                                    color = TextPrimary,
                                    fontSize = 17.sp,
                                    fontWeight = FontWeight.Bold
                                )
                                Text(
                                    text = strings.enrollSub,
                                    color = TextSecondary,
                                    fontSize = 11.sp
                                )
                            }
                        }

                        SheetCloseButton(onClick = onDismiss)
                    }

                    Spacer(modifier = Modifier.height(14.dp))

                    LazyColumn(
                        modifier = Modifier
                            .fillMaxWidth()
                            .weight(1f),
                        verticalArrangement = Arrangement.spacedBy(14.dp)
                    ) {
                        item {
                            FewShotGuidanceCard(description = strings.fewShotGuidanceDesc)
                        }

                        item {
                            EnrollmentIdentitySection(
                                diseaseName = diseaseName,
                                onDiseaseNameChange = { diseaseName = it },
                                hostPlant = hostPlant,
                                onHostPlantChange = { hostPlant = it },
                                adviceText = adviceText,
                                onAdviceTextChange = { adviceText = it },
                                strings = strings
                            )
                        }

                        item {
                            EnrollmentExemplarsSection(
                                capturedPhotos = capturedPhotos,
                                onImportPhotosClick = { launchDiseasedGallery() },
                                onClearAllPhotos = { capturedPhotos.clear() },
                                onRemovePhotoAt = { index ->
                                    if (index < capturedPhotos.size) {
                                        capturedPhotos.removeAt(index)
                                    }
                                },
                                strings = strings
                            )
                        }

                        item {
                            EnrollmentHealthySection(
                                healthyPhotos = healthyPhotos,
                                onImportHealthyPhotos = { launchHealthyGallery() },
                                onClearHealthyPhotos = { healthyPhotos.clear() },
                                onRemoveHealthyPhotoAt = { index ->
                                    if (index < healthyPhotos.size) healthyPhotos.removeAt(index)
                                },
                                strings = strings
                            )
                        }

                        item {
                            val canEnroll = diseaseName.isNotBlank() && capturedPhotos.size >= 1

                            EnrollmentSubmitButton(
                                canEnroll = canEnroll,
                                isCalibrating = isCalibrating,
                                onSubmit = {
                                    if (!isCalibrating && canEnroll) {
                                        isCalibrating = true
                                        onEnroll(
                                            diseaseName.trim(),
                                            hostPlant.trim(),
                                            "",
                                            false,
                                            adviceText.trim(),
                                            capturedPhotos.toList(),
                                            healthyPhotos.toList()
                                        )
                                    }
                                },
                                strings = strings
                            )
                        }

                        if (customClasses.isNotEmpty()) {
                            item {
                                Spacer(modifier = Modifier.height(8.dp))
                                Text(
                                    text = "${strings.activeClasses} (${customClasses.size})",
                                    color = EmeraldAccent,
                                    fontSize = 13.sp,
                                    fontWeight = FontWeight.Bold
                                )
                            }

                            items(customClasses) { cls ->
                                CustomPathologyCard(
                                    cls = cls,
                                    onDelete = { onDeleteClass(cls.id) }
                                )
                            }
                        }
                    }
                }
            }
        }
    }
}
