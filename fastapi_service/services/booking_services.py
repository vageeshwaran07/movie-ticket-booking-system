from datetime import datetime, timezone
from fastapi_service.db.mongo import seats_collection
from fastapi_service.db.seat_model import SeatStatus


def confirm_booking(show_id: int, seat_ids: list, user_id):
    user_id = str(user_id) 
    now = datetime.now(timezone.utc)

    result = seats_collection.update_many(
        {
            "show_id": show_id,
            "seat_id": {"$in": seat_ids},
            "status": SeatStatus.LOCKED,
            "locked_by": user_id,
            "lock_expiry": {"$gt": now},
        },
        {
            "$set": {
                "status": SeatStatus.BOOKED,
                "booked_at": now,
            },
            "$unset": {
                "locked_by": "",
                "lock_expiry": "",
            },
        }
    )

    return result.modified_count == len(seat_ids)
