# API Documentation

## Base URL

```
https://api.example.com/
```

## Authentication

All endpoints except `/auth/login` require a valid JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

## Endpoints

### Authentication

#### POST /auth/login

Authenticate user and get access token.

**Request Body:**
```json
{
    "email": "user@example.com",
    "password": "password123"
}
```

**Response:**
```json
{
    "access_token": "eyJ...",
    "token_type": "bearer"
}
```

### Calls

#### POST /calls/start

Start a new outgoing VoIP call.

**Request Body:**
```json
{
    "phone_number": "+359888123456"
}
```

**Response:**
```json
{
    "id": "uuid",
    "phone_number": "+359888123456",
    "status": "recording",
    "started_at": "2024-01-01T12:00:00Z"
}
```

#### POST /calls/{id}/end

End an ongoing call and trigger AI processing.

**Response:**
```json
{
    "id": "uuid",
    "phone_number": "+359888123456",
    "status": "processing",
    "consent_given": true,
    "duration_seconds": 180,
    "started_at": "2024-01-01T12:00:00Z",
    "ended_at": "2024-01-01T12:03:00Z",
    "created_at": "2024-01-01T12:00:00Z"
}
```

#### GET /calls

Get list of all calls for the authenticated user.

**Response:**
```json
{
    "calls": [
        {
            "id": "uuid",
            "phone_number": "+359888123456",
            "status": "ready",
            "consent_given": true,
            "duration_seconds": 180,
            "started_at": "2024-01-01T12:00:00Z",
            "ended_at": "2024-01-01T12:03:00Z",
            "created_at": "2024-01-01T12:00:00Z"
        }
    ],
    "total": 1
}
```

#### GET /calls/{id}

Get details of a specific call.

**Response:**
```json
{
    "id": "uuid",
    "phone_number": "+359888123456",
    "status": "ready",
    "consent_given": true,
    "duration_seconds": 180,
    "started_at": "2024-01-01T12:00:00Z",
    "ended_at": "2024-01-01T12:03:00Z",
    "created_at": "2024-01-01T12:00:00Z"
}
```

#### GET /calls/{id}/summary

Get AI-generated summary for a specific call.

**Response:**
```json
{
    "summary": "Кратко фактическо резюме на разговора",
    "topics": ["основни теми"],
    "decisions": ["взети решения"],
    "tasks": [
        {
            "task": "конкретна задача",
            "owner": "име или null",
            "deadline": "дата или null"
        }
    ],
    "dates": ["извлечени дати"],
    "amounts": ["извлечени суми"],
    "locations": ["извлечени места"]
}
```

**Error Responses:**
- `400 Bad Request` - Call is still recording
- `202 Accepted` - Summary is still being processed
- `404 Not Found` - Call not found
- `500 Internal Server Error` - AI processing failed

## Call Status Values

| Status | Description |
|--------|-------------|
| `recording` | Call is in progress, being recorded |
| `processing` | Call ended, AI processing in progress |
| `ready` | AI processing complete, summary available |
| `failed` | AI processing failed |

## Error Format

All errors return a JSON response:

```json
{
    "detail": "Error message description"
}
```

## Rate Limits

- 100 requests per minute per user
- 10 concurrent calls per user
