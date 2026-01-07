from datetime import datetime, timezone
from typing import Optional

class SeatStatus:
    AVAILABLE = "AVAILABLE"
    LOCKED = "LOCKED"
    BOOKED = "BOOKED"


def create_seat(
    show_id: int,
    seat_id: str,
    row: str,
    number: int,
    price: int,
):
    return {
        "show_id": show_id,
        "seat_id": seat_id,
        "row": row,
        "number": number,
        "price": price,
        "status": SeatStatus.AVAILABLE,
        "locked_by": None,
        "lock_expiry": None,
        "created_at": datetime.utcnow(timezone.utc),
    }
