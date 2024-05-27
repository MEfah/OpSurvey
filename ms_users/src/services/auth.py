from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt

from settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
datetime_format = "YYYYMMDDThhmmss"


class AuthService():
    """Сервис с функциями, необходимыми при аутентификации и авторизации
    """
    
    def __init__(self):
        pass

    
    def hash_password(self, password: str) -> str:
        """Генерирует хеш пароля

        Args:
            password (str): пароль
            
        Returns:
            str: Хеш пароля
        """
        return pwd_context.hash(password)
    
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Проверяет, что пароль соответствует хешу

        Args:
            plain_password (str): пароль для проверки
            hashed_password (str): хеш пароля пользователя

        Returns:
            bool: пароль верный или нет
        """
        return pwd_context.verify(plain_password, hashed_password)
    
    
    def extract_access_payload(self, token: str) -> dict | None:
        """Извлечь содержимое access-токена

        Args:
            token (str): токен

        Returns:
            dict: содержимое токена
        """
        try:
            # Встроенная проверка на exp
            payload = jwt.decode(token, settings.jwt.access_secret, algorithms='HS256')
        except JWTError:
            return None
        return payload
    
    
    def extract_refresh_payload(self, token: str) -> dict | None:
        """Извлечь содержимое refresh-токена

        Args:
            token (str): токен

        Returns:
            dict: содержимое токена
        """
        try:
            # Встроенная проверка на exp
            payload = jwt.decode(token, settings.jwt.refresh_secret, algorithms='HS256')
        except JWTError:
            return None
        return payload
    
    
    def generate_tokens(self, payload: dict) -> tuple[str, str]:
        """Генерирует access и refresh токены

        Args:
            payload (dict): данные, помещаемые в токен. Автоматически добавляется дата завершения действия

        Returns:
            tuple[str, str]: access-токен, refresh-токен
        """
        access_token = self.__get_jwt_token(payload, settings.jwt.access_secret, timedelta(minutes=settings.jwt.access_ttl_min))
        refresh_token = self.__get_jwt_token(payload, settings.jwt.refresh_secret, timedelta(days=settings.jwt.refresh_ttl_days))
        return access_token, refresh_token
    
    
    def __get_jwt_token(self, data: dict, secret: str, ttl: timedelta) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + ttl
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, secret, algorithm='HS256')
        return encoded_jwt