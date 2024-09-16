from fastapi import APIRouter, Depends

from dependencies.roles import verify_user

router = APIRouter(dependencies=[Depends(verify_user)])

@router.get("/me")
def get_profile():
    return {"hello": "user"}