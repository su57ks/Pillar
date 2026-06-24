package com.example.pillar.network

import retrofit2.Response
import retrofit2.http.GET

interface ApiService {
    @GET("ping")
    suspend fun ping(): Response<String>
}