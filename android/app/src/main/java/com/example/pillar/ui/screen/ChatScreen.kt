package com.example.pillar.ui.screen

import android.util.Log
import androidx.compose.foundation.layout.Column
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel

@Composable
fun ChatScreen(viewModel: MainViewModel = viewModel()) {
    val id by viewModel.selectedId.collectAsState()
    Log.d("UPDATE ID", id.toString())
    val chatDict by viewModel.chatDict.collectAsState()
    val chat = chatDict.chatDict[id]

    if (chat != null) {
        Column() {
            Text(text = chat.user.name)
            Text(text = chat.messages.lastOrNull()?.text ?: "")
        }
    }
}

@Preview
@Composable
private fun ChatScreenPrev() {
    ChatScreen()
}