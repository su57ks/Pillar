package com.example.pillar.ui.screen

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Button
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview

@Composable
fun StartScreen(continueFun: () -> Unit = {}) {
    Column(
        modifier = Modifier
            .fillMaxSize(),
        verticalArrangement = Arrangement.Center,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Text(
            text = "Pillar"
        )
        Text(
            text = "Free open-source \nmessenger"
        )
        Button(
            onClick = {continueFun()}
        ) {
            Text(
                text = "Continue"
            )
        }
    }
}

@Preview
@Composable
private fun StartScreenPrev() {
    StartScreen()
}