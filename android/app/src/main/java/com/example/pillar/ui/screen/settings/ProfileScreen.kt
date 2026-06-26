package com.example.pillar.ui.screen.settings

import androidx.compose.foundation.background
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.ArrowBack
import androidx.compose.material3.Button
import androidx.compose.material3.Icon
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.collectAsState
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.pillar.ui.screen.MainViewModel

@Composable
fun ProfileScreen(viewModel: MainViewModel = viewModel(),
                  toSettings: () -> Unit = {}) {
    val me = viewModel.me.collectAsState().value
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White)
    ) {
        Button(
            onClick = {
                toSettings()
            }
        ) {
            Icon(
                Icons.Default.ArrowBack,
                contentDescription = ""
            )
        }
        Text(text = "Name:\n${me.name}")
        Text(text = "Username:\n${me.username}")
    }
}

@Preview
@Composable
private fun ProfileScreenPrev() {
    ProfileScreen()
}