from fastapi_service.auth import verify_jwt_token


def get_current_user(user=verify_jwt_token):
    return user
