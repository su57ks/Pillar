package com.example.pillar.data

data class Message(
    val time: Long,
    val text: String,
    val read: Boolean = false,
    val senderId: Int,
    val receiverId: Int
)
