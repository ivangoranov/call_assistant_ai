"""
Calls API endpoints.
"""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, HTTPException, status

from app.models.schemas import (
    CallEndRequest,
    CallListResponse,
    CallResponse,
    CallStartRequest,
    CallStartResponse,
    SummaryResponse,
    TaskSchema,
)
from app.workers.ai_processor import process_call_audio

router = APIRouter()

# In-memory storage for MVP (replace with database in production)
_calls_store: dict[str, dict] = {}


@router.post("/start", response_model=CallStartResponse)
async def start_call(
    request: CallStartRequest, background_tasks: BackgroundTasks
) -> CallStartResponse:
    """
    Start a new outgoing VoIP call.

    POST /calls/start
    """
    call_id = str(uuid4())
    now = datetime.utcnow()

    call_data = {
        "id": call_id,
        "phone_number": request.phone_number,
        "status": "recording",
        "consent_given": True,
        "duration_seconds": None,
        "started_at": now,
        "ended_at": None,
        "created_at": now,
    }

    _calls_store[call_id] = call_data

    return CallStartResponse(
        id=call_id,
        phone_number=request.phone_number,
        status="recording",
        started_at=now,
    )


@router.post("/{call_id}/end", response_model=CallResponse)
async def end_call(
    call_id: str,
    background_tasks: BackgroundTasks,
    request: Optional[CallEndRequest] = None,
) -> CallResponse:
    """
    End an ongoing call and trigger AI processing.

    POST /calls/{id}/end
    """
    if call_id not in _calls_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found",
        )

    call_data = _calls_store[call_id]

    if call_data["status"] != "recording":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Call is not in recording state",
        )

    now = datetime.utcnow()
    call_data["ended_at"] = now
    call_data["status"] = "processing"

    if request and request.duration_seconds:
        call_data["duration_seconds"] = request.duration_seconds

    # Trigger background AI processing
    background_tasks.add_task(process_call_audio, call_id)

    return CallResponse(**call_data)


@router.get("", response_model=CallListResponse)
async def list_calls() -> CallListResponse:
    """
    Get list of all calls for the authenticated user.

    GET /calls
    """
    calls = list(_calls_store.values())
    return CallListResponse(
        calls=[CallResponse(**call) for call in calls],
        total=len(calls),
    )


@router.get("/{call_id}", response_model=CallResponse)
async def get_call(call_id: str) -> CallResponse:
    """
    Get details of a specific call.

    GET /calls/{id}
    """
    if call_id not in _calls_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found",
        )

    return CallResponse(**_calls_store[call_id])


@router.get("/{call_id}/summary", response_model=SummaryResponse)
async def get_call_summary(call_id: str) -> SummaryResponse:
    """
    Get AI-generated summary for a specific call.

    GET /calls/{id}/summary
    """
    if call_id not in _calls_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Call not found",
        )

    call_data = _calls_store[call_id]

    if call_data["status"] == "recording":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Call is still recording",
        )

    if call_data["status"] == "processing":
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Summary is still being processed",
        )

    if call_data["status"] == "failed":
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="AI processing failed",
        )

    # Return summary from storage (placeholder for MVP)
    # In production, this would fetch from database
    return SummaryResponse(
        summary="",
        topics=[],
        decisions=[],
        tasks=[],
        dates=[],
        amounts=[],
        locations=[],
    )
