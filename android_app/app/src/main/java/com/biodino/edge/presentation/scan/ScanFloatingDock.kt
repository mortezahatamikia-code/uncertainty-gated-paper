package com.biodino.edge.presentation.scan

import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.horizontalScroll
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.AddCircle
import androidx.compose.material.icons.filled.BatteryChargingFull
import androidx.compose.material.icons.filled.BatterySaver
import androidx.compose.material.icons.filled.Calculate
import androidx.compose.material.icons.filled.CameraAlt
import androidx.compose.material.icons.filled.CheckCircle
import androidx.compose.material.icons.filled.CloudDownload
import androidx.compose.material.icons.filled.History
import androidx.compose.material.icons.filled.LocalFlorist
import androidx.compose.material.icons.filled.PhotoLibrary
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.presentation.theme.BorderHighlight
import com.biodino.edge.presentation.theme.EmeraldAccent
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.ForestSurfaceGlass
import com.biodino.edge.presentation.theme.TextPrimary
import com.biodino.edge.presentation.theme.TextSecondary

@Composable
fun ScanFloatingDock(
    strings: AppStrings,
    isGalleryMode: Boolean,
    isUsingCustomModel: Boolean,
    isEcoMode: Boolean,
    onClearGalleryImage: () -> Unit,
    onLaunchGallery: () -> Unit,
    onOpenAtlas: () -> Unit,
    onOpenCalculator: () -> Unit,
    onOpenHistory: () -> Unit,
    onOpenEnrollment: () -> Unit,
    onOpenModelManager: () -> Unit,
    onToggleEcoMode: () -> Unit,
    modifier: Modifier = Modifier
) {
    val dockScrollState = rememberScrollState()
    Row(
        modifier = modifier
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
        // Live scan
        val isLiveMode = !isGalleryMode
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(if (isLiveMode) EmeraldNeon.copy(alpha = 0.22f) else ForestSurface)
                .border(1.dp, if (isLiveMode) EmeraldNeon else BorderHighlight, RoundedCornerShape(16.dp))
                .clickable { onClearGalleryImage() }
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
                    text = strings.tabLiveScan,
                    color = if (isLiveMode) EmeraldNeon else TextPrimary,
                    fontSize = 11.sp,
                    fontWeight = if (isLiveMode) FontWeight.Bold else FontWeight.Medium
                )
            }
        }

        // Gallery picker
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(if (isGalleryMode) Color(0xFF00B0FF).copy(alpha = 0.22f) else ForestSurface)
                .border(1.dp, if (isGalleryMode) Color(0xFF00B0FF) else BorderHighlight, RoundedCornerShape(16.dp))
                .clickable { onLaunchGallery() }
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
                    text = strings.tabGallery,
                    color = if (isGalleryMode) Color(0xFF00B0FF) else TextPrimary,
                    fontSize = 11.sp,
                    fontWeight = if (isGalleryMode) FontWeight.Bold else FontWeight.SemiBold
                )
            }
        }

        // Atlas
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(ForestSurface)
                .border(1.dp, BorderHighlight, RoundedCornerShape(16.dp))
                .clickable { onOpenAtlas() }
                .padding(horizontal = 10.dp, vertical = 7.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.LocalFlorist, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                Spacer(modifier = Modifier.width(5.dp))
                Text(strings.tabAtlas, color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
            }
        }

        // Dosage calculator
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(ForestSurface)
                .border(1.dp, BorderHighlight, RoundedCornerShape(16.dp))
                .clickable { onOpenCalculator() }
                .padding(horizontal = 10.dp, vertical = 7.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Calculate, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                Spacer(modifier = Modifier.width(5.dp))
                Text(strings.tabDosage, color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
            }
        }

        // History
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(ForestSurface)
                .border(1.dp, BorderHighlight, RoundedCornerShape(16.dp))
                .clickable { onOpenHistory() }
                .padding(horizontal = 10.dp, vertical = 7.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.History, contentDescription = null, tint = TextPrimary, modifier = Modifier.size(17.dp))
                Spacer(modifier = Modifier.width(5.dp))
                Text(strings.tabHistory, color = TextPrimary, fontSize = 11.sp, fontWeight = FontWeight.SemiBold)
            }
        }

        // Custom class enrollment
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(ForestSurface)
                .border(1.dp, BorderHighlight, RoundedCornerShape(16.dp))
                .clickable { onOpenEnrollment() }
                .padding(horizontal = 11.dp, vertical = 7.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.AddCircle, contentDescription = null, tint = EmeraldAccent, modifier = Modifier.size(17.dp))
                Spacer(modifier = Modifier.width(5.dp))
                Text(
                    text = strings.tabEnrollClass,
                    color = EmeraldAccent,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Medium
                )
            }
        }

        // Model manager
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(if (isUsingCustomModel) Color(0xFF00B0FF).copy(alpha = 0.22f) else ForestSurface)
                .border(1.dp, if (isUsingCustomModel) Color(0xFF00B0FF) else BorderHighlight, RoundedCornerShape(16.dp))
                .clickable { onOpenModelManager() }
                .padding(horizontal = 10.dp, vertical = 7.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = if (isUsingCustomModel) Icons.Default.CheckCircle else Icons.Default.CloudDownload,
                    contentDescription = null,
                    tint = if (isUsingCustomModel) Color(0xFF00B0FF) else EmeraldNeon,
                    modifier = Modifier.size(17.dp)
                )
                Spacer(modifier = Modifier.width(5.dp))
                Text(
                    text = if (isUsingCustomModel) strings.tabModelActive else strings.tabModelDownload,
                    color = if (isUsingCustomModel) Color(0xFF00B0FF) else TextPrimary,
                    fontSize = 11.sp,
                    fontWeight = if (isUsingCustomModel) FontWeight.Bold else FontWeight.Medium
                )
            }
        }

        // Eco mode
        Box(
            modifier = Modifier
                .clip(RoundedCornerShape(16.dp))
                .background(if (isEcoMode) EmeraldNeon.copy(alpha = 0.2f) else ForestSurface)
                .border(1.dp, if (isEcoMode) EmeraldNeon else BorderHighlight, RoundedCornerShape(16.dp))
                .clickable { onToggleEcoMode() }
                .padding(horizontal = 9.dp, vertical = 7.dp)
        ) {
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(
                    imageVector = if (isEcoMode) Icons.Default.BatterySaver else Icons.Default.BatteryChargingFull,
                    contentDescription = null,
                    tint = if (isEcoMode) EmeraldNeon else TextSecondary,
                    modifier = Modifier.size(17.dp)
                )
                Spacer(modifier = Modifier.width(5.dp))
                Text(
                    text = strings.tabEcoMode,
                    color = if (isEcoMode) EmeraldNeon else TextSecondary,
                    fontSize = 11.sp,
                    fontWeight = if (isEcoMode) FontWeight.Bold else FontWeight.Medium
                )
            }
        }
    }
}
