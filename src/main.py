import uvicorn
import requests
import uuid
from fastapi import FastAPI, Path
from typing import Optional
from pydantic import BaseModel
from config.config import config


class User(BaseModel):
    name: str
    username: str = uuid.uuid4()
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None

    def toJson(self):
        user = {
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "phone": self.phone,
            "website": self.website,
        }
        return user


class UpdateUser(User, BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[str] = None

    def toJson(self):
        return super().toJson()


app = FastAPI()


@app.get("/")
def index():
    try:
        return {
            "success": True,
            "status": 200,
            "data": {},
            "statusMessages": ["Hola Mundo!"]
        }
    except Exception as e:
        print(f'Error in index, {e}')
        return {
            "success": False,
            "status": 500,
            "data": {},
            "statusMessages": [
                "Internal Server error"
            ]
        }


@app.get("/users")
def get_users(*, start: Optional[int] = 0, limit: Optional[int] = 3):
    try:
        users = requests.get(
            f'{config.API_URL}/users/?_start={start}&_limit={limit}')
        return {
            "success": True,
            "status": users.status_code,
            "data": users.json(),
            "statusMessages": ["Successfully fetched all users"]
        }
    except Exception as e:
        print(f'Error fetching users, {e}')
        return {
            "success": False,
            "status": 500,
            "data": {},
            "statusMessages": [
                "Internal Server error"
            ]
        }


@app.get("/user/{user_id}")
def get_user(user_id: int = Path(None, description="id of the user you want to view", ge=1, lt=333333)):
    try:
        user = requests.get(f'{config.API_URL}/users/{user_id}')
        if user.ok:
            return {
                "success": True,
                "status": user.status_code,
                "data": [user.json()],
                "statusMessages": ["Successfully fetched user details"]
            }
        return {
            "success": False,
            "status": 404,
            "data": {},
            "statusMessages": ["No user found with the given id"]
        }
    except Exception as e:
        print(f'Error fetching user, {e}')
        return {
            "success": False,
            "status": 500,
            "data": {},
            "statusMessages": [
                "Internal Server error"
            ]
        }


@app.post("/add-user")
def add_user(user: User):
    try:
        if not user.name:
            return {
                "success": False,
                "status": 401,
                "data": {},
                "statusMessages": [
                    "Cannot create a user"
                ]
            }
        new_user = requests.post(f'{config.API_URL}/users', json=user.toJson())
        return {
            "success": True,
            "status": new_user.status_code,
            "data": new_user.json(),
            "statusMessages": [
                "Successfully created a new user"
            ]
        }
    except Exception as e:
        print(f'Error adding user, {e}')
        return {
            "success": False,
            "status": 500,
            "data": {},
            "statusMessages": [
                "Internal Server error"
            ]
        }


@app.put("/users/{user_id}")
def update_user(user_id: int, user: UpdateUser):
    try:
        user_exists = requests.get(f'{config.API_URL}/users/{user_id}')
        if user_exists.ok:
            payload = {
                **user_exists.json(),
                **user.toJson()
            }
            updated_user = requests.put(
                f'{config.API_URL}/users/{user_id}', json=payload)
            return {
                "success": True,
                "status": updated_user.status_code,
                "data": updated_user.json(),
                "statusMessages": [
                    "Successfully updated user"
                ],
            }
        return {
            "success": False,
            "status": 404,
            "data": {},
            "statusMessages": ["No user found with the given id"]
        }
    except Exception as e:
        print(f'Error updating user, {e}')
        return {
            "success": False,
            "status": 500,
            "data": {},
            "statusMessages": [
                "Internal Server error"
            ]
        }


@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    try:
        user_exists = requests.get(f'{config.API_URL}/users/{user_id}')
        if user_exists.ok:
            removed_user = requests.delete(
                f'{config.API_URL}/users/{user_id}')
            return {
                "success": True,
                "status": removed_user.status_code,
                "data": removed_user.json(),
                "statusMessages": [
                    "Successfully deleted a user"
                ],
            }
        return {
            "success": False,
            "status": 404,
            "data": {},
            "statusMessages": ["No user found with the given id"]
        }
    except Exception as e:
        print(f'Error deleting users, {e}')
        return {
            "success": False,
            "status": 500,
            "data": {},
            "statusMessages": [
                "Internal Server error"
            ]
        }


if __name__ == "__main__":
    uvicorn.run("main:app", host=config.HOST,
                port=config.PORT, log_level=config.LOG_LEVEL)
