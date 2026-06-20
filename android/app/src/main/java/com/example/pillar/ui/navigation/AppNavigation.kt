package com.example.pillar.ui.navigation

import android.util.Log
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.example.pillar.ui.screen.ChatScreen
import com.example.pillar.ui.screen.MainScreen
import com.example.pillar.ui.screen.SettingsScreen

@Composable
fun AppNavHost() {
    val nav = rememberNavController()
    NavHost(navController = nav, startDestination = "main") {
        composable("main"){ MainScreen(
            toSettings = {nav.navigate("settings")},
            toChat = {nav.navigate("chat")}
        ) }
        composable("settings"){ SettingsScreen()}
        composable("chat") { ChatScreen() }
    }
}