#!/usr/bin/env python3
"""
auth.py
Authentication module
"""
import uuid
from os import getenv
from typing import Any

import bcrypt
import redis
from backend.app.models import Admin
from backend.app.schemas import AdminLogin
from dotenv import load_dotenv
from sqlalchemy.orm import Session

load_dotenv()

REDIS_URL = getenv("REDIS_URL")
# Connect to Redis
r = redis.StrictRedis.from_url(REDIS_URL)


def _hash_password(password: str) -> bytes:
    """ hash the password """
    encoded = password.encode('utf-8')
    return bcrypt.hashpw(encoded, bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate UUIDs"""
    return str(uuid.uuid4())


class Auth:
    """ Class providing authentication functionalities """

    def __init__(self, db: Session):
        """Initialize a new DB instance
        """
        self.__current_user = None
        self._db = db

    def authorization_header(self, request=None) -> Any | None:
        """ Retrieve Authorization header """
        if request is not None:
            return request.headers.get('Authorization', None)


    def register_user(self, admin:AdminLogin) -> Admin:
        """ Register a new user """
        username = admin.username
        try:
            if self._db.query(Admin).filter(Admin.username == username).first() is not None:
                raise ValueError("Email already registered")

            # Hash the password
            hashed_password = _hash_password(admin.password).decode('utf-8')  # Access password directly

            # Create a new Admin object with the data from the AdminLogin model
            user = Admin(username=admin.username, hashed_password=hashed_password)
            self._db.add(user)
            self._db.commit()
            self._db.refresh(user)

            return username
        except Exception as e:
            raise Exception(f"Error registering user {admin.username}: {str(e)}")

    def valid_login(self, kwargs) -> str | bool:
        """ Validate login credentials """
        username = kwargs.username
        password = kwargs.password
        user = self._db.query(Admin).filter(Admin.username == username).first()
        if user:
            if bcrypt.checkpw(password.encode('utf-8'),
                                  user.hashed_password.encode('utf-8')):
                return self.__create_session(user)
        return False

    def __create_session(self, user):
        """ Create a new session """
        try:
            session_id = _generate_uuid()
            key = f"auth_{session_id}"
            r.set(key, str(user.username), ex=3600)
            return session_id
        except Exception as e:
            raise Exception(f"Error creating session for {user.username}: {str(e)}")


    def get_user_from_session_id(self, session_id: str) -> str:
        """ Retrieve user based on session ID """
        try:
            return r.get(f"auth_{session_id}")
        except Exception as e:
            raise Exception(f"Error getting user from"
                            f" session id {session_id}: {str(e)}")


    def destroy_session(self, session_id) -> None:
        """ Destroy user session """
        try:
            r.delete(f"auth_{session_id}")
        except Exception as e:
            raise Exception(f"Error destroying session"
                            f" for {session_id}: {str(e)}")
