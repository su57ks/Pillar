package com.example.pillar.ui.screen

import android.support.v4.os.ResultReceiver
import android.util.Log
import androidx.lifecycle.ViewModel
import com.example.pillar.data.Chat
import com.example.pillar.data.Message
import com.example.pillar.data.User
import com.example.pillar.data.ChatDict
import com.example.pillar.network.PillarApi
import com.example.pillar.ui.theme.PillarTheme
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

class MainViewModel : ViewModel() {
    private val _chatDict = MutableStateFlow(
        ChatDict(
            chatDict = mapOf(
                1 to Chat(
                    user = User(
                        id = 1,
                        name = "Aizen",
                        username = "Aizen"

                    ),
                    messages = listOf(
                        Message(
                            time = 3600000,
                            text = "Привет! Как дела? У меня все круто, вот недавно с Гином разговаривал",
                            read = true,
                            senderId = 1,
                            receiverId = 2
                        ),
                        Message(
                            time = 3600000,
                            text = "Плохо",
                            read = true,
                            senderId = 2,
                            receiverId = 1
                        )
                    )
                )
            )
        )
    )
    val chatDict: StateFlow<ChatDict> = _chatDict.asStateFlow()

    fun updateUser(chatId: Int, chatData: Chat) {
        _chatDict.update { currentDict ->
            ChatDict(currentDict.chatDict + (chatId to chatData))
        }
    }

    fun newMessage(text: String, senderId: Int, time: Long, receiverId: Int){
        _chatDict.update { currentDict ->
            val chat = currentDict.chatDict[receiverId]
            if (chat != null) {
                val message = Message(
                    receiverId = receiverId,
                    senderId = senderId,
                    time = time,
                    text = text
                )
                val updatedMessages = chat.messages + message
                val updatedChat = chat.copy(messages = updatedMessages)
                ChatDict(currentDict.chatDict + (receiverId to updatedChat))
            } else {
                currentDict
            }
        }
    }

    private val _selectedId = MutableStateFlow(0)
    val selectedId: StateFlow<Int> = _selectedId.asStateFlow()

    fun updateId(id: Int) {
        _selectedId.value = id
        Log.d("UPDATE ID", _selectedId.value.toString())
        Log.d("UPDATE ID", selectedId.value.toString())
    }

    private val _me = MutableStateFlow(
        User(
            id = 2,
            name = "Orihime",
            username = "Orihime"
        )
    )
    val me: StateFlow<User> = _me.asStateFlow()

    private val _net = MutableStateFlow("")
    val net: StateFlow<String> = _net.asStateFlow()

    fun updateUrl(url: String){
        _net.value = url
    }
}