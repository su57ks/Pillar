package com.example.pillar.ui.screen

import android.util.Log
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material3.Button
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import com.example.pillar.network.PillarApi
import kotlinx.coroutines.launch

@Composable
fun ServerScreen() {
    var ip by remember { mutableStateOf("") }
    var port by remember { mutableStateOf("") }
    val scope = rememberCoroutineScope()
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Connection"
        )
        OutlinedTextField(
            value = ip,
            onValueChange = {ip = it},
            label = {
                Text(
                    text = "IP"
                )
            }
        )
        OutlinedTextField(
            value = port,
            onValueChange = {port = it},
            label = {
                Text(
                    text = "Port"
                )
            }
        )
        Button(
            onClick = {
                scope.launch {
                    val result = PillarApi.retrofit.ping()
                    Log.d("API", result.body().toString())
                }
            }
        ) {
            Text("Connect")
        }
    }
}

@Preview
@Composable
private fun ServerScreenPrev() {
    ServerScreen()
}