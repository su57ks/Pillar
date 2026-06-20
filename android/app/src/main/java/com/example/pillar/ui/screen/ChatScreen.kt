package com.example.pillar.ui.screen

import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview

@Composable
fun ChatScreen(modifier: Modifier = Modifier) {
    Text("Random chat")
}

@Preview
@Composable
private fun ChatScreenPrev() {
    ChatScreen()
}