from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Booking, BookingSeat
from users.models import User

@api_view(["POST"])
def save_booking(request):
    data = request.data

    user = User.objects.get(id=data["user_id"])

    booking = Booking.objects.create(
        user=user,
        show_id=data["show_id"],
        total_amount=data["total_amount"],
        payment_id=data["payment_id"],
        status="CONFIRMED",
    )

    for seat in data["seats"]:
        BookingSeat.objects.create(
            booking=booking,
            seat_id=seat["seat_id"],
            price=seat["price"],
        )

    return Response({
        "booking_id": booking.id,
        "status": "CONFIRMED"
    })
