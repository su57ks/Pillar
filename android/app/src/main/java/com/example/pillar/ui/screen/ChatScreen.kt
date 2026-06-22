package com.example.pillar.ui.screen

import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun ChatScreen(viewModel: MainViewModel = viewModel()) {
    val id by viewModel.selectedId.collectAsState()
    val userDict by viewModel.userDict.collectAsState()
    val user = userDict.userDict[id]

    if (user != null) {
        Column() {
            Text(text = user.name)
            Text(text = user.messages.lastOrNull()?.text ?: "")
        }
    }
}

@Preview
@Composable
private fun ChatScreenPrev() {
    ChatScreen()
}