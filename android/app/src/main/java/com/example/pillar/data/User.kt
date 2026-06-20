package com.example.pillar.data

data class User(
    val name: String,
    val username: String,
    val id: Int,
    val messages: List<Message> = emptyList()
)
