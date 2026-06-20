package com.example.pillar.ui.screen

import androidx.lifecycle.ViewModel
import com.example.pillar.data.User
import com.example.pillar.data.UserDict
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update

class MainViewModel: ViewModel() {
    private val _userDict = MutableStateFlow(UserDict())
    val userDict: StateFlow<UserDict> = _userDict.asStateFlow()

    fun updateUser(userId: Int, userData: User) {
        _userDict.update { currentDict ->
            UserDict(currentDict.userDict + (userId to userData))
        }

    }
    private val _selectedId = MutableStateFlow(0)
    val selectedId: StateFlow<Int> = _selectedId.asStateFlow()
}