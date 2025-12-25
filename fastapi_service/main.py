from fastapi import FastAPI
from fastapi_service.routers import booking, seats, payments, test_db
from fastapi.security import HTTPBearer
from fastapi_service.db.mongo import create_ttl_index

app = FastAPI()
security = HTTPBearer()
app.include_router(booking.router)

app.include_router(payments.router)

app.include_router(seats.router)
app.include_router(test_db.router)


@app.on_event("startup")
def startup_event():
    create_ttl_index()