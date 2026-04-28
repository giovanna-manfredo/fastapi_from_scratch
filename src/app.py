from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database import get_session
from src.models import User
from src.schemas import SchemaUser, SchemaUserPublic

app = FastAPI()


@app.get("/users/", status_code=HTTPStatus.OK, response_model=list[SchemaUser])
def list_users(
    skip: int = 0, limit: int = 100, session: Session = Depends(get_session)
):
    users = session.scalars(select(User).offset(skip).limit(limit)).all()
    return users


@app.get("/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.scalar(select(User).where((User.id == user_id)))
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found",
        )

    return user


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=SchemaUserPublic)
def create_user(user: SchemaUserPublic, session: Session = Depends(get_session)):
    user_exist = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )
    if user_exist:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="This user already exists",
        )

    new_user = User(username=user.username, email=user.email)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@app.put("/users/{user_id}", response_model=SchemaUserPublic)
def update_user(
    user_id: int, user: SchemaUserPublic, session: Session = Depends(get_session)
):

    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    try:
        db_user.username = user.username
        db_user.email = user.email
        session.commit()
        session.refresh(db_user)

        return db_user

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Username or Email already exists"
        )


@app.delete("/users/{user_id}")
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.scalar(select(User).where(User.id == user_id))

    if not db_user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="User not found")

    session.delete(db_user)
    session.commit()

    return {"message": "User deleted"}
