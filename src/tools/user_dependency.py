from fastapi import Request

def get_current_user(request: Request):
    return {
        "auth_type": request.state.auth_type,
        "user_id": request.state.user_id,
    }