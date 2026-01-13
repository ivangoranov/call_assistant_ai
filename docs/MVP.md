# MVP Documentation

## Overview

This document describes the Minimum Viable Product (MVP) for the AI Call Summarizer application.

## MVP Scope

### In Scope

1. **Calls**
   - Outgoing calls only
   - VoIP-based calling via SIP
   - Automatic call recording
   - Consent message played before connection: "Разговорът се записва с цел организация."

2. **Recording**
   - Format: WAV
   - One audio file per call
   - Stored in object storage

3. **Transcription**
   - Language: Bulgarian
   - Model: Whisper (or equivalent)
   - Plain text output

4. **AI Summarization**
   - Structured JSON output
   - Bulgarian language only
   - Facts-only extraction

5. **Android App**
   - Login screen
   - Dialer (VoIP)
   - Call history
   - Call details with summary and tasks

### Out of Scope

- iOS support
- Incoming calls
- CRM features
- Calendar integration
- Email or sharing
- Payments
- Multi-user teams
- Analytics dashboards

## Call Lifecycle

```
recording → processing → ready
                      ↘ failed
```

## Data Model

- `users` - User accounts
- `calls` - Call metadata
- `transcripts` - Raw transcription text
- `summaries` - AI-generated summaries
- `tasks` - Extracted tasks from calls

## Non-Functional Requirements

- Async background processing for AI
- Environment-based configuration
- Structured logging
- Versioned AI prompts
- Clear separation of concerns

## Definition of Done

- [ ] A real VoIP call can be made
- [ ] Call audio is recorded
- [ ] Bulgarian transcription is generated
- [ ] AI summary + tasks are created
- [ ] Results are visible in Android app
