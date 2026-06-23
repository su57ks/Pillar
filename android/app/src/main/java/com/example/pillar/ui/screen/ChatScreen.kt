package com.example.pillar.ui.screen

import android.util.Log
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.height
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.width
import androidx.compose.foundation.layout.widthIn
import androidx.compose.foundation.layout.wrapContentWidth
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.rememberLazyListState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.material3.TextField
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Alignment.Companion
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalConfiguration
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.tooling.preview.Preview
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.pillar.data.Message
import com.example.pillar.utils.messageTime

@Composable
fun ChatScreen(viewModel: MainViewModel = viewModel(), toMain: () -> Unit = {}) {
    val screenHeight = LocalConfiguration.current.screenHeightDp.dp
    val maxHeight = screenHeight * 0.05f
    var input by remember { mutableStateOf("") }
    val id by viewModel.selectedId.collectAsState()
    Log.d("UPDATE ID", id.toString())
    val chatDict by viewModel.chatDict.collectAsState()
    val chat = chatDict.chatDict[id]
    val me = viewModel.me.collectAsState().value.id

    val listState = rememberLazyListState()
    LaunchedEffect(chat?.messages?.size) {
        if (chat?.messages?.isNotEmpty() ?: false) {
            listState.animateScrollToItem(chat?.messages?.size ?: 0)
        }
    }

    if (chat != null) {
        Column(
            modifier = Modifier.fillMaxSize(),

            ) {
            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .background(Color.Green),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.Start
            ) {
                Button(
                    onClick = {
                        viewModel.updateId(0)
                        toMain()
                    }) {
                    Icon(
                        Icons.Default.ArrowBack, contentDescription = ""
                    )
                }
                Spacer(modifier = Modifier.width(10.dp))
                Text(text = chat.user.name)
            }

            LazyColumn(
                state = listState,
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(8f)
                    .background(Color.White),
                verticalArrangement = Arrangement.Bottom,
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                items(
                    items = chat.messages
                ) { message ->
                    Message(message = message, viewModel = viewModel)
                }

            }


            Row(
                modifier = Modifier
                    .fillMaxWidth()
                    .weight(1f)
                    .background(Color.Green)
                    .clip(RoundedCornerShape(20.dp)),
                verticalAlignment = Alignment.CenterVertically,
                horizontalArrangement = Arrangement.End
            ) {
                TextField(
                    value = input,
                    onValueChange = { input = it },
                    modifier = Modifier
                        .fillMaxWidth(0.8f)
                        .height(maxHeight),
                    shape = RoundedCornerShape(20.dp)
                )
                Button(
                    onClick = {
                        if (input != "") {
                            viewModel.newMessage(
                                text = input, receiverId = id, senderId = me, time = 1
                            )
                            input = ""
                        }
                    }) {
                    Icon(
                        Icons.Default.PlayArrow, contentDescription = ""
                    )

                }
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
        contentAlignment = if (message.senderId == viewModel.me.collectAsState().value.id) {
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
            Column() {
                Text(
                    text = message.text
                )
                Text(
                    text = messageTime(message.time), modifier = Modifier.align(Alignment.End)
                )
            }
        }
    }
}