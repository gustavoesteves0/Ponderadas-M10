from fastapi import APIRouter, HTTPException
from typing import List
from models.models import User
from schemas.schemas import UserSchema, UserCreate

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=UserSchema, status_code=201)
async def create_user(user: UserCreate):
    existing_user = await User.objects.get_or_none(email=user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    user_obj = await User.objects.create(**user.dict())
    return user_obj

@router.get("/", response_model=List[UserSchema])
async def list_users():
    return await User.objects.all()


@router.get("/{user_id}", response_model=UserSchema)
async def get_user(user_id: int):
    user = await User.objects.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user_data: UserCreate):
    user = await User.objects.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user.update(**user_data.dict())
    updated_user = await User.objects.get(id=user_id)
    return updated_user


@router.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    user = await User.objects.get_or_none(id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user.delete()
    return
