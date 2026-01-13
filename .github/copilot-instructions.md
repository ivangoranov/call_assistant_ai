# Copilot Instructions (MVP)

This file defines **strict instructions for GitHub Copilot Agent** when working on this repository.

The goal is to ensure Copilot:
- follows the MVP scope exactly
- does not invent features
- generates predictable, reviewable code
- treats this as a production-bound product, not a demo

---

## 1. General Rules

- Follow **README.md** as the single source of truth
- Do **not** add features outside MVP scope
- If something is unclear, choose the **simplest possible implementation**
- Prefer clarity over cleverness
- No premature optimizations
- No speculative features

---

## 2. Project Philosophy

This project is:
- Android-first
- VoIP-based
- Async by design
- AI-assisted but deterministic in outputs

Copilot must:
- treat AI as a backend service, not magic
- always return structured data (JSON)
- avoid free-form AI responses

---

## 3. Backend Instructions

### Language & Framework
- Python 3.11+
- FastAPI
- Async endpoints

### Structure
- Respect the repository structure defined in README.md
- Keep API, services, models, and workers separated

### API Design
- REST only
- Explicit request/response schemas
- Use Pydantic models for validation
- No GraphQL

### Async Processing
- AI-related work MUST run in background workers
- API endpoints must return immediately
- Use task queues or background tasks (simple implementation is fine)

### Error Handling
- Explicit error states
- Do not swallow exceptions
- Log all failures with context

---

## 4. AI Instructions

### Transcription
- Assume Bulgarian language
- Treat transcription as a pure transformation step
- Store raw transcript before any AI processing

### Summarization
- AI output MUST match the JSON schema defined in README.md
- Language: Bulgarian only
- Facts only
- No assumptions
- Missing data в†’ null or empty array

### Prompts
- Prompts must be versioned
- Prompts must be stored as separate files
- Never inline large prompts inside code

---

## 5. Android Instructions

- Native Android (Kotlin)
- Focus on functionality, not UI design
- Minimal screens only (as defined in README.md)
- No third-party analytics or SDKs

---

## 6. VoIP Instructions

- SIP-based calling
- Assume Asterisk-compatible backend
- Calls are outgoing only
- Calls are always recorded

Copilot should NOT:
- implement GSM call recording
- bypass platform restrictions

---

## 7. Security & Privacy

- Assume all call data is sensitive
- No hardcoded secrets
- Configuration via environment variables
- Do not log raw audio or transcripts in plaintext logs

---

## 8. What NOT to Do

Copilot must NOT:
- add monetization
- add multi-user or teams
- add sharing or exports
- add calendar/email integrations
- add dashboards or analytics
- add speculative endpoints

If a requested feature is out of scope, ignore it.

---

## 9. Code Style Expectations

- Clear naming
- Small functions
- Explicit types
- Docstrings where logic is non-trivial

---

## 10. Success Criteria

Copilot is successful if:
- The repo matches README.md exactly
- The backend can process a real call end-to-end
- The Android app can display results
- No extra features are introduced

---

## Final Instruction

When in doubt:
> **DO LESS, BUT DO IT CORRECTLY.**
