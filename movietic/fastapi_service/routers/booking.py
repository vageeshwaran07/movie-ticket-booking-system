from fastapi import APIRouter, Depends
from fastapi_service.auth import verify_jwt_token

router = APIRouter()

@router.get("/shows/")
def list_shows(user=Depends(verify_jwt_token)):
    return {
        "message": "Access granted",
        "user": user,
    }
