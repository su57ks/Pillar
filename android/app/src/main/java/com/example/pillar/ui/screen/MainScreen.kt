package com.example.pillar.ui.screen

import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.material3.Button
import androidx.compose.material3.ButtonDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.pillar.data.ChatDict

@OptIn(ExperimentalFoundationApi::class)
@Composable
fun MainScreen(toSettings: () -> Unit = {}, toChat: () -> Unit = {}, viewModel: MainViewModel = viewModel()) {
    val chatDict by viewModel.chatDict.collectAsState()
    val userIds = chatDict.chatDict.keys.toList()
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        verticalArrangement = Arrangement.Top,
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        stickyHeader {
            Text(text = "su57ks")
            Row() {
                Button(
                    onClick = {}
                ) {
                    Text(text = "Чаты")
                }
                Button(
                    onClick = {
                        toSettings()
                              },
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Color.Gray
                    )
                ) {
                    Text(text = "Настройки")
                }
            }
        }
        for (id in userIds) {
            item { Chat(chatDict = chatDict, id = id, onClick = toChat, viewModel = viewModel) }
            item { HorizontalDivider(color = Color.Black) }
        }
    }
}

@Preview
@Composable
private fun MainScreenPrev() {
    MainScreen()
}

@Composable
fun Chat(chatDict: ChatDict, id: Int, onClick: () -> Unit, viewModel: MainViewModel) {
    val chat = chatDict.chatDict[id]
    if (chat != null) {
        Row(
            modifier = Modifier
                .background(Color.LightGray)
                .fillMaxWidth()
                .padding(5.dp)
                .clickable {
                    viewModel.updateId(id)
                    onClick()
                }
        ) {
            Column() {
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        text = chat.user.name,
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.fillMaxWidth(0.7f)
                    )
                    Text(chat.messages.lastOrNull()?.time?.toString() ?: "")
                }
                Row(
                    modifier = Modifier.fillMaxWidth(),
                    horizontalArrangement = Arrangement.SpaceBetween
                ) {
                    Text(
                        chat.messages.lastOrNull()?.text ?: "",
                        maxLines = 1,
                        overflow = TextOverflow.Ellipsis,
                        modifier = Modifier.fillMaxWidth(0.6f)
                    )
                }
            }
        }
    }
}