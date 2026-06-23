package com.example.pillar.ui.navigation

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.lifecycle.viewmodel.compose.viewModel
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.pillar.ui.screen.ChatScreen
import com.example.pillar.ui.screen.MainScreen
import com.example.pillar.ui.screen.MainViewModel
import com.example.pillar.ui.screen.SettingsScreen

@Composable
fun AppNavHost() {
    val viewModel: MainViewModel = viewModel()

    val nav = rememberNavController()
    NavHost(navController = nav, startDestination = "main") {
        composable("main"){ MainScreen(
            toSettings = {nav.navigate("settings")},
            toChat = {nav.navigate("chat")},
            viewModel = viewModel
        ) }
        composable("settings"){ SettingsScreen(
            toMain = {nav.navigate("main")}
        )}
        composable("chat") { ChatScreen(
            viewModel = viewModel,
            toMain = {nav.navigate("main")}
        ) }
    }
}