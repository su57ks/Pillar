package com.example.pillar.ui.screen

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview

@Composable
fun SettingsScreen(toMain: () -> Unit = {},
                   toProfile: () -> Unit = {}) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Row() {
            Button(
                onClick = {
                    toMain()
                },
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color.Gray
                )
            ) {
                Text(text = "Чаты")
            }
            Button(
                onClick = {}
            ) {
                Text(text = "Настройки")
            }
        }
        Button(
            onClick = {
                toProfile()
            }
        ) {
            Text(text = "Profile")
        }
    }
}

@Preview
@Composable
private fun SettingsScreenPrev() {
    SettingsScreen()
}