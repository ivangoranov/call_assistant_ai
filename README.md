# # AI Call Summarizer (MVP)

Android-first VoIP application that records phone calls, transcribes them in **Bulgarian**, and generates **AI-powered summaries and task lists**.

This project is built as an MVP for real-world usage (personal + small organizations such as cultural institutions), with future SaaS scalability in mind.

---

## 1. Product Goal

The system must:
- Make **outgoing VoIP phone calls**
- Automatically **record each call**
- Transcribe the audio to **Bulgarian text**
- Generate a **structured AI summary**
- Extract **tasks, dates, amounts, and locations**
- Display results in a minimal Android UI

---

## 2. Platform & Tech Stack

### Mobile
- Android (native)
- Kotlin
- SIP / VoIP client integration

### Backend
- Python 3.11+
- FastAPI
- Async REST API

### AI
- Speech-to-Text: Whisper (Bulgarian)
- Summarization: LLM (structured JSON output)

### VoIP
- SIP
- Asterisk (or compatible SIP server)

### Storage
- PostgreSQL (metadata)
- Object storage (WAV audio files)

---

## 3. MVP Scope (IN SCOPE)

### 3.1 Calls
- Outgoing calls only
- Calls are initiated from the Android app
- All calls go through the VoIP backend
- Each call:
  - is automatically recorded
  - is marked as `consent_given = true`
- Before call connection, an audio message is played:
  > вЂњР Р°Р·РіРѕРІРѕСЂСЉС‚ СЃРµ Р·Р°РїРёСЃРІР° СЃ С†РµР» РѕСЂРіР°РЅРёР·Р°С†РёСЏ.вЂќ

---

### 3.2 Recording
- Format: WAV
- One audio file per call
- Stored in object storage
- Backend stores file reference only

---

### 3.3 Transcription
- Language: **Bulgarian**
- Model: Whisper (or equivalent)
- Output: plain text
- No speaker diarization in MVP
- No punctuation correction beyond model defaults

---

### 3.4 AI Summarization

From the transcription, generate a **structured JSON** with the following schema:

```json
{
  "summary": "РљСЂР°С‚РєРѕ С„Р°РєС‚РёС‡РµСЃРєРѕ СЂРµР·СЋРјРµ РЅР° СЂР°Р·РіРѕРІРѕСЂР°",
  "topics": ["РѕСЃРЅРѕРІРЅРё С‚РµРјРё"],
  "decisions": ["РІР·РµС‚Рё СЂРµС€РµРЅРёСЏ"],
  "tasks": [
    {
      "task": "РєРѕРЅРєСЂРµС‚РЅР° Р·Р°РґР°С‡Р°",
      "owner": "РёРјРµ РёР»Рё null",
      "deadline": "РґР°С‚Р° РёР»Рё null"
    }
  ],
  "dates": ["РёР·РІР»РµС‡РµРЅРё РґР°С‚Рё"],
  "amounts": ["РёР·РІР»РµС‡РµРЅРё СЃСѓРјРё"],
  "locations": ["РёР·РІР»РµС‡РµРЅРё РјРµСЃС‚Р°"]
}
```

Rules:
- Output must be **valid JSON**
- Language: **Bulgarian only**
- Extract **facts only**
- Do not invent or assume information
- If something is missing, return `null` or empty arrays

---

### 3.5 Backend API

Backend is a **REST API**, async, with background workers for AI processing.

#### Required endpoints:
- `POST /auth/login`
- `POST /calls/start`
- `POST /calls/{id}/end`
- `GET /calls`
- `GET /calls/{id}`
- `GET /calls/{id}/summary`

#### Call lifecycle statuses:
- `recording`
- `processing`
- `ready`
- `failed`

AI processing must never block API requests.

---

### 3.6 Data Model (Minimum)

Tables:
- `users`
- `calls`
- `transcripts`
- `summaries`
- `tasks`

No organizations, teams, or sharing in MVP.

---

### 3.7 Android App (MVP UI)

Screens:
1. Login
2. Dialer (VoIP)
3. Call History
4. Call Details
   - Audio playback
   - AI summary
   - Task list

UI requirements:
- Minimal
- Functional
- No design system required
- Focus on correctness, not visuals

---

## 4. Out of Scope (Explicitly NOT in MVP)

- iOS support
- Incoming calls
- CRM features
- Calendar integration
- Email or sharing
- Payments
- Multi-user teams
- Analytics dashboards

---

## 5. Non-Functional Requirements

- Async background processing for AI
- Environment-based configuration (`.env`)
- Structured logging
- Versioned AI prompts
- Clear separation of concerns (API / services / workers)

---

## 6. Repository Structure (Expected)

```
/backend
  /app
    /api
    /models
    /services
    /workers
  main.py
  requirements.txt

/android
  /app
  build.gradle

/docs
  MVP.md
  API.md
```

---

## 7. Definition of Done (MVP)

- A real VoIP call can be made
- Call audio is recorded
- Bulgarian transcription is generated
- AI summary + tasks are created
- Results are visible in Android app

---

## 8. Target Usage

- Internal usage
- Real conversations
- Validation of usefulness for organizers and professionals

This MVP prioritizes **correctness, reliability, and real-world value** over features.
