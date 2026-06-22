package com.example.pillar.ui.screen

import android.util.Log
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.wrapContentWidth
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Alignment.Companion
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.pillar.data.Message

@Composable
fun ChatScreen(viewModel: MainViewModel = viewModel()) {
    val id by viewModel.selectedId.collectAsState()
    Log.d("UPDATE ID", id.toString())
    val chatDict by viewModel.chatDict.collectAsState()
    val chat = chatDict.chatDict[id]
    if (chat != null) {
        Text(text = chat.user.name)
        Column(
            modifier = Modifier
                .fillMaxSize()
                .background(Color.White),
            verticalArrangement = Arrangement.Bottom,
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            for (message in chat.messages) {
                Message(message = message, viewModel = viewModel)
            }
        }
    }
}

@Preview
@Composable
private fun ChatScreenPrev() {
    val viewModel: MainViewModel = viewModel()
    viewModel.updateId(1)
    ChatScreen()
}

@Composable
fun Message(message: Message, viewModel: MainViewModel) {
    val screenWidth = LocalConfiguration.current.screenWidthDp.dp
    val maxWidth = screenWidth * 0.7f

    Box(
        modifier = Modifier
            .fillMaxWidth()
            .background(Color.Transparent)
            .padding(2.dp),
        contentAlignment =
            if (message.senderId == viewModel.me.collectAsState().value.id) {
                Alignment.CenterEnd
            } else {
                Alignment.CenterStart
            }
    ) {
        Box(
            modifier = Modifier
                .wrapContentWidth()
                .widthIn(max = maxWidth)
                .background(Color.Gray)
                .padding(10.dp)

        ) {
            Text(
                text = message.text
            )
        }
    }
}