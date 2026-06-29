from fastapi import HTTPException


def throw_404(detail :str):
    return HTTPException(
        status_code=404,
        detail=detail)


def throw_409(detail: str):
    return HTTPException(
        status_code=409,
        detail=detail)


def throw_500():
    return HTTPException(
        status_code=500,
        detail="Something went wrong")
