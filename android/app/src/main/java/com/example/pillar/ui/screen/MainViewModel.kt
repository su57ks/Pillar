package com.example.pillar.ui.screen

import android.util.Log
import androidx.lifecycle.ViewModel
import com.example.pillar.data.Chat
import com.example.pillar.data.Message
import com.example.pillar.data.User
import com.example.pillar.data.ChatDict
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
                            text = "Привет! Как дела?",
                            read = true,
                            senderId = 1,
                            receiverId = 2
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

    private val _selectedId = MutableStateFlow(0)
    val selectedId: StateFlow<Int> = _selectedId.asStateFlow()

    fun updateId(id: Int) {
        _selectedId.value = id
        Log.d("UPDATE ID", _selectedId.value.toString())
        Log.d("UPDATE ID", selectedId.value.toString())
    }
}