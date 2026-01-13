package com.callassistant.ai.api

import com.callassistant.ai.data.CallResponse
import com.callassistant.ai.data.CallStartRequest
import com.callassistant.ai.data.CallStartResponse
import com.callassistant.ai.data.LoginRequest
import com.callassistant.ai.data.SummaryResponse
import com.callassistant.ai.data.TokenResponse
import retrofit2.Response
import retrofit2.http.Body
import retrofit2.http.GET
import retrofit2.http.POST
import retrofit2.http.Path

/**
 * Retrofit API service interface for AI Call Summarizer backend.
 */
interface ApiService {

    /**
     * POST /auth/login
     * Authenticate user and get access token.
     */
    @POST("auth/login")
    suspend fun login(@Body request: LoginRequest): Response<TokenResponse>

    /**
     * POST /calls/start
     * Start a new outgoing VoIP call.
     */
    @POST("calls/start")
    suspend fun startCall(@Body request: CallStartRequest): Response<CallStartResponse>

    /**
     * POST /calls/{id}/end
     * End an ongoing call.
     */
    @POST("calls/{id}/end")
    suspend fun endCall(@Path("id") callId: String): Response<CallResponse>

    /**
     * GET /calls
     * Get list of all calls.
     */
    @GET("calls")
    suspend fun getCalls(): Response<List<CallResponse>>

    /**
     * GET /calls/{id}
     * Get details of a specific call.
     */
    @GET("calls/{id}")
    suspend fun getCall(@Path("id") callId: String): Response<CallResponse>

    /**
     * GET /calls/{id}/summary
     * Get AI-generated summary for a call.
     */
    @GET("calls/{id}/summary")
    suspend fun getCallSummary(@Path("id") callId: String): Response<SummaryResponse>
}
