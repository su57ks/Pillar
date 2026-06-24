package com.example.pillar.network

import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path

interface ApiService {
    @GET("ping/{time}")
    suspend fun ping(@Path("time") time: Int = 1): Response<String>
}