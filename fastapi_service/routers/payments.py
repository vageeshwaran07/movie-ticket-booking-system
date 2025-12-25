from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, timezone
from fastapi_service.db.mongo import seats_collection
from fastapi_service.db.seat_model import SeatStatus
from fastapi_service.auth import verify_jwt_token
from fastapi_service.services.booking_services import confirm_booking
import uuid
import razorpay
import os

from dotenv import load_dotenv
load_dotenv()
router = APIRouter(prefix="/payment", tags=["Payment"])



@router.post("/initiate")
def initiate_payment(payload: dict, user=Depends(verify_jwt_token)):
    show_id = payload.get("show_id")
    seat_ids = payload.get("seats")

    if not show_id or not seat_ids or not isinstance(seat_ids, list):
        raise HTTPException(status_code=400, detail="Invalid request")

    now = datetime.now(timezone.utc)

    locked_seats = list(seats_collection.find({
        "show_id": show_id,
        "seat_id": {"$in": seat_ids},
        "status": SeatStatus.LOCKED,
        "locked_by": user["user_id"],
        "lock_expiry": {"$gt": now},
    }))

    if len(locked_seats) != len(seat_ids):
        raise HTTPException(
            status_code=409,
            detail="Seat lock expired or invalid",
        )

    total_amount = sum(seat["price"] for seat in locked_seats)

    return {
        "payment_intent_id": str(uuid.uuid4()),
        "amount": total_amount,
        "currency": "INR",
        "expires_at": max(seat["lock_expiry"] for seat in locked_seats),
        "message": "Payment initiated successfully",
    }


@router.post("/webhook")
def payment_webhook(payload: dict):
    payment_status = payload.get("status")
    show_id = payload.get("show_id")
    seat_ids = payload.get("seats")
    user_id = str(payload.get("user_id"))

    if payment_status != "SUCCESS":
        raise HTTPException(status_code=400, detail="Payment failed")

    success = confirm_booking(show_id, seat_ids, user_id)

    if not success:
        raise HTTPException(
            status_code=409,
            detail="Seat lock expired, booking rejected",
        )

    return {
        "message": "Booking confirmed successfully",
        "show_id": show_id,
        "seats": seat_ids,
    }

client = razorpay.Client(
    auth=(
        os.getenv("RAZORPAY_KEY_ID"),
        os.getenv("RAZORPAY_KEY_SECRET")
    )
)

@router.post("/create-order")
def create_order(payload: dict, user=Depends(verify_jwt_token)):


    amount = payload["amount"] * 100  # Razorpay uses paise

    order = client.order.create({
        "amount": amount,
        "currency": "INR",
        "payment_capture": 1
    })

    return {
        "order_id": order["id"],
        "amount": order["amount"],
        "currency": order["currency"],
        "key": os.getenv("RAZORPAY_KEY_ID")
    }

@router.post("/verify-payment")
def verify_payment(payload: dict):

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": payload["razorpay_order_id"],
            "razorpay_payment_id": payload["razorpay_payment_id"],
            "razorpay_signature": payload["razorpay_signature"],
        })
    except:
        raise HTTPException(status_code=400, detail="Payment verification failed")

@router.post("/verify")
def verify_payment(payload: dict):
    # 🚧 TEMP TEST MODE
    # Assume payment success

    return {
        "message": "Payment verified (test mode)",
        "payment_id": payload.get("razorpay_payment_id", "test_payment")
    }
