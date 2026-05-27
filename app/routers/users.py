from fastapi import APIRouter
from data.db import SessionDep
from schemas.users import UserDB, UserPublic
from sqlmodel import select

users_router = APIRouter(prefix="/users")

@users_router.get("/")
def get_al_users(session: SessionDep) -> list(UserPublic):
    """Return all users"""
    users = session.exec(select(UserDB)).all()
    return users

