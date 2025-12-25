from fastapi import APIRouter
from fastapi_service.db.mongo import seats_collection

router = APIRouter()

@router.get("/test-mongo")
def test_mongo():
    return {
        "count": seats_collection.count_documents({})
    }
