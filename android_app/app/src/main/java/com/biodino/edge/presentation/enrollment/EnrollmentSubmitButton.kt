package com.biodino.edge.presentation.enrollment

import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.RocketLaunch
import androidx.compose.material3.*
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.biodino.edge.data.locale.AppStrings
import com.biodino.edge.presentation.theme.EmeraldNeon
import com.biodino.edge.presentation.theme.ForestDark
import com.biodino.edge.presentation.theme.ForestSurface
import com.biodino.edge.presentation.theme.TextSecondary

@Composable
fun EnrollmentSubmitButton(
    canEnroll: Boolean,
    isCalibrating: Boolean,
    onSubmit: () -> Unit,
    strings: AppStrings,
    modifier: Modifier = Modifier
) {
    Button(
        onClick = onSubmit,
        enabled = canEnroll && !isCalibrating,
        colors = ButtonDefaults.buttonColors(
            containerColor = EmeraldNeon,
            contentColor = ForestDark,
            disabledContainerColor = ForestSurface,
            disabledContentColor = TextSecondary
        ),
        shape = RoundedCornerShape(14.dp),
        modifier = modifier
            .fillMaxWidth()
            .height(46.dp)
    ) {
        if (isCalibrating) {
            CircularProgressIndicator(
                modifier = Modifier.size(20.dp),
                color = ForestDark,
                strokeWidth = 2.dp
            )
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = strings.calibratingExtracting,
                fontSize = 12.sp,
                fontWeight = FontWeight.Bold
            )
        } else {
            Icon(Icons.Default.RocketLaunch, contentDescription = null, modifier = Modifier.size(18.dp))
            Spacer(modifier = Modifier.width(8.dp))
            Text(
                text = strings.btnCalibrateEnroll,
                fontSize = 13.sp,
                fontWeight = FontWeight.Bold
            )
        }
    }
}

