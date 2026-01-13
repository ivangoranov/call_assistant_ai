package com.callassistant.ai.data

/**
 * Data classes for API request/response models.
 * Mirrors the backend Pydantic schemas.
 */

// Auth
data class LoginRequest(
    val email: String,
    val password: String
)

data class TokenResponse(
    val access_token: String,
    val token_type: String
)

// Calls
data class CallStartRequest(
    val phone_number: String
)

data class CallStartResponse(
    val id: String,
    val phone_number: String,
    val status: String,
    val started_at: String
)

data class CallResponse(
    val id: String,
    val phone_number: String,
    val status: String,
    val consent_given: Boolean,
    val duration_seconds: Int?,
    val started_at: String,
    val ended_at: String?,
    val created_at: String
)

// Summary (matches AI output JSON schema)
data class TaskItem(
    val task: String,
    val owner: String?,
    val deadline: String?
)

data class SummaryResponse(
    val summary: String,
    val topics: List<String>,
    val decisions: List<String>,
    val tasks: List<TaskItem>,
    val dates: List<String>,
    val amounts: List<String>,
    val locations: List<String>
)
