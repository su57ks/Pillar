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
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.rememberCoroutineScope
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.tooling.preview.Preview
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.pillar.network.PillarApi
import kotlinx.coroutines.launch

@Composable
fun LoginScreen(viewModel: MainViewModel = viewModel(), onClick: () -> Unit = {}) {
    var login by remember { mutableStateOf("") }
    var password by remember { mutableStateOf("") }
    val scope = rememberCoroutineScope()
    val url = viewModel.net.collectAsState().value
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Login"
        )
        OutlinedTextField(
            value = login,
            onValueChange = {login = it},
            label = {
                Text(
                    text = "Login"
                )
            }
        )
        OutlinedTextField(
            value = password,
            onValueChange = {password = it},
            label = {
                Text(
                    text = "Password"
                )
            }
        )
        Button(
            onClick = {
                scope.launch {
                    Log.d("API", url)
                    try {
                        val result = PillarApi(url).retrofit.login(login = login, password = password)
                        if (result.isSuccessful) {
                            Log.d("API", result.body().toString())
                            if (result?.body() == "true"){
                                onClick()
                            }
                        }
                    }
                    catch (e: Exception)
                    {
                        Log.d("API", "error")
                    }
                }
            }
        ) {
            Text("Login")
        }
    }
}

@Preview
@Composable
private fun LoginScreenPrev() {
    LoginScreen()
}