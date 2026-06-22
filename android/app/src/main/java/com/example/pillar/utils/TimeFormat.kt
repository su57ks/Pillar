package com.example.pillar.utils

fun messageTime(time: Long): String {
    val millisecondsToday = time % 86400000
    val hours = (millisecondsToday / 3600000).toInt()
    val minutes = (millisecondsToday % 3600000 / 60000).toInt()
    val seconds = (millisecondsToday % 60000 / 1000).toInt()
    return String.format("%02d:%02d:%02d", hours, minutes, seconds)
}