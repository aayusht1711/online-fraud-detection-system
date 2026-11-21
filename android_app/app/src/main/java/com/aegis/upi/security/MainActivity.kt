package com.aegis.upi.security

import android.content.Context
import android.hardware.display.DisplayManager
import android.os.Bundle
import android.os.Handler
import android.os.Looper
import android.telephony.TelephonyManager
import android.view.Display
import android.view.WindowManager
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontFamily
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class MainActivity : ComponentActivity() {

    private lateinit var displayManager: DisplayManager
    private lateinit var telephonyManager: TelephonyManager

    // Observable states for Jetpack Compose
    private val isRealScreenSharing = mutableStateOf(false)
    private val isRealCallActive = mutableStateOf(false)
    private val isSimulatedScreenSharing = mutableStateOf(false)
    private val isSimulatedCallActive = mutableStateOf(false)
    private val showSecurityDisclaimer = mutableStateOf(false)
    private val showSuccessDialog = mutableStateOf(false)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // 1. HARDWARE ZERO-TOLERANCE SHIELD: Pitch-black display in AnyDesk / TeamViewer / Mirroring
        window.setFlags(
            WindowManager.LayoutParams.FLAG_SECURE,
            WindowManager.LayoutParams.FLAG_SECURE
        )

        displayManager = getSystemService(Context.DISPLAY_SERVICE) as DisplayManager
        telephonyManager = getSystemService(Context.TELEPHONY_SERVICE) as TelephonyManager

        // Initial hardware scan
        updateHardwareSensors()

        // 2. REAL HARDWARE LISTENER: Detects when AnyDesk, TeamViewer, or Zoom starts screen casting
        displayManager.registerDisplayListener(object : DisplayManager.DisplayListener {
            override fun onDisplayAdded(displayId: Int) {
                updateHardwareSensors()
            }
            override fun onDisplayRemoved(displayId: Int) {
                updateHardwareSensors()
            }
            override fun onDisplayChanged(displayId: Int) {
                updateHardwareSensors()
            }
        }, Handler(Looper.getMainLooper()))

        setContent {
            MaterialTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color(0xFF0F172A)
                ) {
                    UpiPaymentScreen(
                        isScreenSharing = isRealScreenSharing.value || isSimulatedScreenSharing.value,
                        isCallActive = isRealCallActive.value || isSimulatedCallActive.value,
                        isSimScreen = isSimulatedScreenSharing.value,
                        isSimCall = isSimulatedCallActive.value,
                        onToggleSimScreen = { isSimulatedScreenSharing.value = !isSimulatedScreenSharing.value },
                        onToggleSimCall = { isSimulatedCallActive.value = !isSimulatedCallActive.value },
                        onPayClicked = {
                            val threat = (isRealScreenSharing.value || isSimulatedScreenSharing.value ||
                                          isRealCallActive.value || isSimulatedCallActive.value)
                            if (threat) {
                                showSecurityDisclaimer.value = true
                            } else {
                                showSuccessDialog.value = true
                            }
                        }
                    )

                    // Authentic Google Pay Security Disclaimer Dialog
                    if (showSecurityDisclaimer.value) {
                        AlertDialog(
                            onDismissRequest = { showSecurityDisclaimer.value = false },
                            title = {
                                Text(
                                    text = "⚠️ Google Pay Security Alert",
                                    fontWeight = FontWeight.Bold,
                                    color = Color(0xFFF43F5E),
                                    fontSize = 18.sp
                                )
                            },
                            text = {
                                Text(
                                    text = "Screen sharing or an active phone call was detected.\n\n" +
                                           "For your financial protection, Google Pay does not permit UPI payments or PIN entry while an app (e.g., AnyDesk, TeamViewer) is viewing your screen or while you are on a call.\n\n" +
                                           "Please close AnyDesk / stop screen sharing and disconnect the call to proceed.",
                                    color = Color(0xFFCBD5E1),
                                    fontSize = 14.sp
                                )
                            },
                            confirmButton = {
                                Button(
                                    onClick = { showSecurityDisclaimer.value = false },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFE11D48))
                                ) {
                                    Text("Exit & Withhold PIN", color = Color.White, fontWeight = FontWeight.Bold)
                                }
                            },
                            containerColor = Color(0xFF1E293B)
                        )
                    }

                    // Success dialog
                    if (showSuccessDialog.value) {
                        AlertDialog(
                            onDismissRequest = { showSuccessDialog.value = false },
                            title = {
                                Text("✅ Payment Authorized", color = Color(0xFF10B981), fontWeight = FontWeight.Bold)
                            },
                            text = {
                                Text("No screen-sharing or active call detected. Transaction completed securely via Aegis Zero-Trust Shield.", color = Color(0xFFCBD5E1))
                            },
                            confirmButton = {
                                Button(
                                    onClick = { showSuccessDialog.value = false },
                                    colors = ButtonDefaults.buttonColors(containerColor = Color(0xFF10B981))
                                ) {
                                    Text("Done", color = Color.White)
                                }
                            },
                            containerColor = Color(0xFF1E293B)
                        )
                    }
                }
            }
        }
    }

    override fun onResume() {
        super.onResume()
        updateHardwareSensors()
    }

    private fun updateHardwareSensors() {
        // AnyDesk and screen-sharing apps create a secondary VirtualDisplay
        val displays = displayManager.displays
        val sharingActive = displays.any { display ->
            display.displayId != Display.DEFAULT_DISPLAY &&
            (display.flags and Display.FLAG_SECURE == 0)
        }
        isRealScreenSharing.value = sharingActive

        // Phone call state
        try {
            val callState = telephonyManager.callState
            isRealCallActive.value = (callState != TelephonyManager.CALL_STATE_IDLE)
        } catch (_: Exception) {
            // Handled if permission hasn't been granted yet
        }
    }
}

@Composable
fun UpiPaymentScreen(
    isScreenSharing: Boolean,
    isCallActive: Boolean,
    isSimScreen: Boolean,
    isSimCall: Boolean,
    onToggleSimScreen: () -> Unit,
    onToggleSimCall: () -> Unit,
    onPayClicked: () -> Unit
) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(20.dp),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.SpaceBetween
    ) {
        Column(horizontalAlignment = Alignment.CenterHorizontally) {
            // Header
            Text(
                text = "Google Pay",
                fontSize = 24.sp,
                fontWeight = FontWeight.ExtraBold,
                color = Color.White,
                modifier = Modifier.padding(top = 16.dp)
            )
            Text(
                text = "Protected by Aegis Pre-PIN Fraud Defense",
                fontSize = 12.sp,
                color = Color(0xFF38BDF8),
                modifier = Modifier.padding(bottom = 20.dp)
            )

            // Live Sensor Status Card
            Card(
                shape = RoundedCornerShape(16.dp),
                colors = CardDefaults.cardColors(
                    containerColor = if (isScreenSharing || isCallActive) Color(0xFF450A0A) else Color(0xFF064E3B)
                ),
                modifier = Modifier.fillMaxWidth().padding(bottom = 16.dp)
            ) {
                Column(modifier = Modifier.padding(16.dp)) {
                    Text(
                        text = if (isScreenSharing || isCallActive) "🚨 ACTIVE COERCION THREAT" else "🛡️ DISPLAY SECURE (FLAG_SECURE)",
                        fontWeight = FontWeight.Bold,
                        fontSize = 14.sp,
                        color = if (isScreenSharing || isCallActive) Color(0xFFFCA5A5) else Color(0xFF6EE7B7)
                    )
                    Spacer(modifier = Modifier.height(4.dp))
                    Text(
                        text = buildString {
                            if (isScreenSharing) append("• Screen Sharing / Mirroring Active (AnyDesk Hooked)\n")
                            if (isCallActive) append("• Active Phone Call in Progress (Telephony Hooked)\n")
                            if (!isScreenSharing && !isCallActive) append("• No external displays or ongoing phone calls detected. Safe to pay.")
                        }.trimEnd(),
                        fontSize = 12.sp,
                        color = Color(0xFFE2E8F0)
                    )
                }
            }

            // Payment Target Card
            Card(
                shape = RoundedCornerShape(20.dp),
                colors = CardDefaults.cardColors(containerColor = Color(0xFF1E293B)),
                modifier = Modifier.fillMaxWidth()
            ) {
                Column(
                    modifier = Modifier.padding(20.dp),
                    horizontalAlignment = Alignment.CenterHorizontally
                ) {
                    Text(text = "Paying", fontSize = 12.sp, color = Color(0xFF94A3B8))
                    Text(
                        text = "Rahul Gear Stores",
                        fontSize = 18.sp,
                        fontWeight = FontWeight.Bold,
                        color = Color.White
                    )
                    Text(
                        text = "rahulgear@okaxis",
                        fontSize = 12.sp,
                        fontFamily = FontFamily.Monospace,
                        color = Color(0xFF38BDF8)
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(
                        text = "₹ 2,499.00",
                        fontSize = 32.sp,
                        fontWeight = FontWeight.ExtraBold,
                        color = Color.White
                    )
                }
            }
        }

        // Action Section
        Column(
            modifier = Modifier.fillMaxWidth(),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            // Testing Toggles (allows testing even without a second phone)
            Text(
                text = "Live Hardware & Testing Simulator:",
                fontSize = 11.sp,
                color = Color(0xFF94A3B8),
                modifier = Modifier.padding(bottom = 8.dp)
            )
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Button(
                    onClick = onToggleSimScreen,
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isSimScreen) Color(0xFFE11D48) else Color(0xFF334155)
                    ),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text(
                        text = if (isSimScreen) "Screen: SHARING" else "Test AnyDesk",
                        fontSize = 11.sp,
                        textAlign = TextAlign.Center
                    )
                }
                Button(
                    onClick = onToggleSimCall,
                    modifier = Modifier.weight(1f),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = if (isSimCall) Color(0xFFE11D48) else Color(0xFF334155)
                    ),
                    shape = RoundedCornerShape(12.dp)
                ) {
                    Text(
                        text = if (isSimCall) "Call: ACTIVE" else "Test Call",
                        fontSize = 11.sp,
                        textAlign = TextAlign.Center
                    )
                }
            }

            Spacer(modifier = Modifier.height(12.dp))

            // Main Pay Button
            Button(
                onClick = onPayClicked,
                modifier = Modifier
                    .fillMaxWidth()
                    .height(54.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = if (isScreenSharing || isCallActive) Color(0xFFE11D48) else Color(0xFF10B981)
                ),
                shape = RoundedCornerShape(16.dp)
            ) {
                Text(
                    text = if (isScreenSharing || isCallActive) "🔒 Payment Locked (Coercion Active)" else "Pay ₹ 2,499 with UPI",
                    fontWeight = FontWeight.Bold,
                    fontSize = 15.sp,
                    color = Color.White
                )
            }
            Spacer(modifier = Modifier.height(16.dp))
        }
    }
}
