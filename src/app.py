from http import HTTPStatus

from fastapi import FastAPI

from src.schemas import User, UserPublic

app = FastAPI()


@app.get("/users/", status_code=HTTPStatus.OK, response_class=list[UserPublic])
def list_users():
    ...

@app.get("/users/{user_id}", status_code=HTTPStatus.OK)
def get_user(user_id: int):
    ...

@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: User):
    ...

