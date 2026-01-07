from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timedelta, timezone
from fastapi_service.db.mongo import seats_collection
from fastapi_service.db.seat_model import SeatStatus
from fastapi_service.auth import verify_jwt_token

router = APIRouter(prefix="/seats", tags=["Seats"])


@router.post("/lock")
def lock_seats(payload: dict, user=Depends(verify_jwt_token)):
    show_id = payload.get("show_id")
    seat_ids = payload.get("seats")

    if not show_id or not seat_ids or not isinstance(seat_ids, list):
        raise HTTPException(status_code=400, detail="Invalid request")

    lock_expiry = datetime.now(timezone.utc) + timedelta(minutes=5)

    result = seats_collection.update_many(
        {
            "show_id": show_id,
            "seat_id": {"$in": seat_ids},
            "status": SeatStatus.AVAILABLE,
        },
        {
            "$set": {
                "status": SeatStatus.LOCKED,
                "locked_by": user["user_id"],
                "lock_expiry": lock_expiry,
            }
        }
    )

    if result.modified_count != len(seat_ids):
        seats_collection.update_many(
            {
                "show_id": show_id,
                "seat_id": {"$in": seat_ids},
                "locked_by": user["user_id"],
            },
            {
                "$set": {"status": SeatStatus.AVAILABLE},
                "$unset": {"locked_by": "", "lock_expiry": ""},
            }
        )
        raise HTTPException(
            status_code=409,
            detail="One or more seats are not available",
        )

    return {
        "message": "Seats locked successfully",
        "expires_at": lock_expiry,
    }
