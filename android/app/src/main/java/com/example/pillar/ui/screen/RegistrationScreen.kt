package com.example.pillar.ui.screen

import android.util.Log
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.height
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
import androidx.compose.ui.unit.dp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.pillar.network.PillarApi
import kotlinx.coroutines.launch

@Composable
fun RegistrationScreen(viewModel: MainViewModel = viewModel(),
                       onClick: () -> Unit = {},
                       toLogin: () -> Unit = {}) {
    var login by remember { mutableStateOf("") }
    var password1 by remember { mutableStateOf("") }
    var password2 by remember { mutableStateOf("") }
    val url = viewModel.net.collectAsState().value
    val scope = rememberCoroutineScope()
    Column(
        modifier = Modifier
            .fillMaxSize()
            .background(Color.White),
        horizontalAlignment = Alignment.CenterHorizontally,
        verticalArrangement = Arrangement.Center
    ) {
        Text(
            text = "Registration"
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
            value = password1,
            onValueChange = {password1 = it},
            label = {
                Text(
                    text = "Password1"
                )
            }
        )
        OutlinedTextField(
            value = password2,
            onValueChange = {password2 = it},
            label = {
                Text(
                    text = "Password2"
                )
            }
        )
        Button(
            onClick = {
                scope.launch {
                    Log.d("API", url)
                    try {
                        val result = PillarApi(url).retrofit.registration(login = login, password = password1)
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
            Text("Register")
        }
        Spacer(modifier = Modifier.height(15.dp))
        Text(
            text = "Already have an account? Login",
            modifier = Modifier.clickable{toLogin()},
            color = Color.Blue
            )
    }
}

@Preview
@Composable
private fun RegistrationScreenPrev() {
    RegistrationScreen()
}