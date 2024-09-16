from fastapi import APIRouter, Depends

from dependencies.roles import verify_admin

router = APIRouter(dependencies=[Depends(verify_admin)])

@router.get("/manageusers")
def get_profile():
    return {"manage": "users"}