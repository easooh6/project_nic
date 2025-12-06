from fastapi import APIRouter, Depends, HTTPException, status, Query
from src.domain.booking.booking_service import BookingService
from src.presentation.di.service.auth.verify import get_verify_access
from src.domain.dto.auth.token import TokenDTO

from src.presentation.routers.booking.requests.hold import BookingHoldRequest
from src.presentation.routers.booking.requests.confirm import BookingConfirmRequest
from src.presentation.routers.booking.responses.hold_response import BookingHoldResponse
from src.presentation.routers.booking.responses.booking_response import BookingResponse
from src.presentation.routers.booking.responses.me import BookingMeResponse, BookingMeItem
from src.presentation.routers.booking.responses.availability_response import AvailabilityResponse
from datetime import date

from src.domain.exceptions.booking.booking import (
    TimeSlotUnavailableException,
    HoldAlreadyExistsException,
    BookingNotFoundException,
    BookingCancelForbiddenException,
    HoldNotFoundException,
    SlotCollisionException
)

router = APIRouter()

@router.post("/hold", response_model=BookingHoldResponse, status_code=status.HTTP_200_OK)
async def hold_slot(payload: BookingHoldRequest, user: TokenDTO = Depends(get_verify_access)):
    """Удержинеие слотов"""
    try:
        service = BookingService()
        result = await service.hold(
            resource_id=payload.resource_id,
            starts_at=payload.starts_at,
            ends_at=payload.ends_at,
            user_id=user.sub
        )
        return BookingHoldResponse(**result)
    except TimeSlotUnavailableException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except HoldAlreadyExistsException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@router.post("/confirm", response_model=BookingResponse, status_code=status.HTTP_200_OK)
async def confirm_booking(payload: BookingConfirmRequest, user: TokenDTO = Depends(get_verify_access)):
    try:
        service = BookingService()
        result = await service.confirm(user_id=user.sub, hold_id=payload.hold_id)
        return BookingResponse(**result.model_dump())
    except HoldNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except SlotCollisionException as e:
        raise HTTPException(status_code=409, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@router.post("/{booking_id}/cancel", status_code=status.HTTP_200_OK)
async def cancel_booking(booking_id: int, user: TokenDTO = Depends(get_verify_access)):
    try:
        service = BookingService()
        await service.cancel(user_id=user.sub, booking_id=booking_id)
        return {"status": "cancelled"}
    except BookingNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except BookingCancelForbiddenException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {e}")

@router.get("/me", response_model=BookingMeResponse, status_code=status.HTTP_200_OK)
async def get_my_bookings(user: TokenDTO = Depends(get_verify_access)):
    service = BookingService()
    items = await service.get_my_bookings(user.sub)

    response = BookingMeResponse(
        bookings=[BookingMeItem(**b.model_dump()) for b in items]
    )
    return response

@router.get("/{resource_id}/availability", response_model=AvailabilityResponse)
async def get_availability(resource_id: int, date_param: date = Query(..., alias="date")):
    service = BookingService()
    
    slots = await service.get_availability(resource_id, date_param)
    return AvailabilityResponse(slots=slots)

