from jose import JWTError, jwt
from settings import settings


class AuthService():
    """Сервис с функциями, необходимыми при аутентификации и авторизации
    """
    
    def __init__(self):
        pass
    
    
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