from datetime import datetime, timedelta
from typing import Union, Any

from fastapi import HTTPException
from fastapi.requests import Request
from jose import jwt
from passlib.context import CryptContext

from config import SECRET_JWT, SECRET_JWT_REFRESH


class Password:
    def __init__(self):
        self.password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, password: str) -> str:
        return self.password_context.hash(password)

    def verify(self, password: str, hashed_pass: str) -> bool:
        return self.password_context.verify(password, hashed_pass)

    @staticmethod
    def check(password: str) -> bool:
        if len(password) < 8:
            raise HTTPException(status_code=400, detail="Пароль должен содержать минимум 8 символов.")
        if password.isdigit():
            raise HTTPException(status_code=400,
                                detail="Пароль должен содержать минимум 2 буквы разных регистров.")
        if password.islower():
            raise HTTPException(status_code=400,
                                detail="Пароль должен содержать минимум 2 буквы разных регистров.")
        if password.isupper():
            raise HTTPException(status_code=400,
                                detail="Пароль должен содержать минимум 2 буквы разных регистров.")
        if password.isalnum():
            raise HTTPException(status_code=400,
                                detail="Пароль должен содержать минимум 1 специальный символ.")
        if password.isalpha():
            raise HTTPException(status_code=400,
                                detail="Пароль должен содержать минимум минимум 1 цифру.")
        return True


class Token:
    def __init__(self):
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
        self.REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 * 2  # 14 days
        self.ALGORITHM = "HS256"
        self.JWT_SECRET_KEY = SECRET_JWT
        self.JWT_REFRESH_SECRET_KEY = SECRET_JWT_REFRESH

    def create_access(self, subject: Union[str, Any]) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.JWT_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    def create_refresh(self, subject: Union[str, Any]) -> str:
        expires_delta = datetime.utcnow() + timedelta(minutes=self.REFRESH_TOKEN_EXPIRE_MINUTES)
        to_encode = {"exp": expires_delta, "sub": str(subject)}
        encoded_jwt = jwt.encode(to_encode, self.JWT_REFRESH_SECRET_KEY, self.ALGORITHM)
        return encoded_jwt

    async def check(self, request: Request, type_: bool = True) -> dict:
        try:
            try:
                authorization = request.headers.get("Authorization").split(" ")
            except AttributeError:
                raise HTTPException(
                    status_code=400,
                    detail="Отсутствует заголовок с токеном."
                )
            if authorization[0] != "Selezenka":
                raise HTTPException(status_code=400, detail="Не угадал.")
            if type_:
                payload = jwt.decode(authorization[1], self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
            else:
                payload = jwt.decode(authorization[1], self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
            if datetime.fromtimestamp(payload["exp"]) < datetime.now():
                raise HTTPException(
                    status_code=401,
                    detail="Срок действия токена истёк."
                )
        except jwt.JWTError:
            raise HTTPException(
                status_code=403,
                detail="Не удалось подтвердить учетные данные."
            )
        return payload
