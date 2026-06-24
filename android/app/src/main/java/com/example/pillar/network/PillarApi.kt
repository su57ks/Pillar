package com.example.pillar.network

import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory

class PillarApi(url: String = "http://10.0.2.2:8080/") {
    var BASE_URL = url

    val retrofit: ApiService by lazy {
        Retrofit.Builder()
            .baseUrl(BASE_URL)
            .addConverterFactory(GsonConverterFactory.create())
            .build()
            .create(ApiService::class.java)
    }
}