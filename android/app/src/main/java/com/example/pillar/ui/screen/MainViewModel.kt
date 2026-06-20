package com.example.pillar.ui.screen

import androidx.lifecycle.ViewModel
import com.example.pillar.data.User
import com.example.pillar.data.UserList
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow

class MainViewModel: ViewModel() {
    private val _userList = MutableStateFlow(UserList())
    val userList: StateFlow<UserList> = _userList.asStateFlow()

    fun updateUser(userId: Int, userData: User){
        for (user in _userList.value.userList){
            if (user.id == userId){
                //
            }
        }
    }

    private val _selectedId = MutableStateFlow(0)
    val selectedId: StateFlow<Int> = _selectedId.asStateFlow()
}