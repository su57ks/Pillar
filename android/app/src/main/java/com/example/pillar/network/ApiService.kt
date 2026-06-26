package com.example.pillar.network

import retrofit2.Response
import retrofit2.http.GET
import retrofit2.http.Path

interface ApiService {
    @GET("ping/{time}")
    suspend fun ping(@Path("time") time: Int = 1): Response<String>

    @GET("login/{login}/{password}")
    suspend fun login(@Path("login") login: String, @Path("password") password: String): Response<String>

    @GET("registration/{login}/{password}")
    suspend fun registration(@Path("login") login: String, @Path("password") password: String): Response<String>
}