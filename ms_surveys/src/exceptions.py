from typing import Any, Dict, List, Optional, Union
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from httpx import Response
from starlette.responses import JSONResponse
from builtins import AssertionError
import re



class ApiHTTPException(HTTPException):
    """Обработка ошибок API"""

    status_code: int
    code: str
    detail: str

    def __init__(
        self, status_code: Optional[int] = None, detail: Any = None
    ) -> None:
        status_code = status_code or self.status_code
        detail = detail or self.detail
        super().__init__(status_code=status_code, detail=detail)


class UnauthorizedException(ApiHTTPException):
    """Неавторизован"""

    def __init__(
        self, detail: Any = None
    ) -> None:
        self.status_code = status.HTTP_401_UNAUTHORIZED
        self.code = "unauthorized"
        self.detail = detail or "Unauthorized"


class ForbiddenException(ApiHTTPException):
    """Доступ запрещен"""

    def __init__(
        self, detail: Any = None
    ) -> None:
        self.status_code = status.HTTP_403_FORBIDDEN
        self.code = "forbidden"
        self.detail = detail or "Forbidden"
        
        
class NotFoundException(ApiHTTPException):
    """Объект не найден"""
    
    def __init__(
        self, detail: Any = None
    ) -> None:
        self.status_code = status.HTTP_404_NOT_FOUND
        self.code = "not_found"
        self.detail = detail or "Not found"


class ConflictException(ApiHTTPException):
    """Конфликт"""
    
    def __init__(
        self, location: Any = None, description: Any = 'Конфликт'
    ) -> None:
        self.status_code = status.HTTP_409_CONFLICT
        self.code = "conflict"
        self.detail = {
                "location": location,
                "detail": description
            }


class UnprocessableEntityException(ApiHTTPException):
    """Ошибки валидации"""

    def __init__(
        self, detail: Any = None
    ) -> None:
        self.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        self.code = "unprocessable_entity"
        self.detail = detail or "Unprocessable entity"


def setup_exception_handlers(app: FastAPI) -> None:
    """Назначение обработчиков исключений

    Args:
        app (FastAPI): Fasp api приложение
    """

    @app.exception_handler(IntegrityError)
    async def integrity_error(
        request: Request, exc: IntegrityError
    ) -> JSONResponse:
        """
        Обработка ошибок нарушения уникальности ключей в бд
        """
        match = re.search(r'Key \(.*?\)', str(exc))
        if match:
            location = match.group(0)[5:-1]
        else:
            location = None
        
        return api_http_exception(ConflictException(location=location))

    @app.exception_handler(RequestValidationError)
    async def validation_error(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        """
        Обработка ошибок валидации
        """
        errors = exc.errors()
        for e in errors:
            if 'ctx' in e and 'error' in e['ctx'] and isinstance(e['ctx']['error'], AssertionError):
                e['ctx']['error'] = 'Assertion error'
        return api_http_exception(UnprocessableEntityException(detail=errors))

    @app.exception_handler(ApiHTTPException)
    async def handle_api_exceptions(
        request: Request, exc: ApiHTTPException
    ) -> JSONResponse:
        """
        Обработка ошибок API
        """
        return api_http_exception(exc)

    @app.exception_handler(Exception)
    async def handle_exceptions(request: Request, exc: Exception) -> JSONResponse:
        """
        Обработка ошибок API
        """
        return api_exception(exc)


def api_http_exception(exc: ApiHTTPException) -> JSONResponse:
    """
    Форматирование исключения для ответа в API.

    :param exc:
    :return:
    """
    return JSONResponse(
        status_code=exc.status_code,
        content=format_exception(exc.code, exc.detail),
    )


def api_exception(exc: Exception) -> JSONResponse:
    """
    Форматирование общих исключений для ответа в API.

    :param exc:
    :return:
    """

    code = "server_error"
    description = "Внутренняя ошибка сервера."

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=format_exception(code, description),
    )


def format_exception(code: str, description: Union[str, Dict]) -> Dict:
    """Форматирование исключения

    Args:
        code (str): строка код ошибки
        description (Union[str, Dict]): описание ошибки

    Returns:
        Dict: Форматированное исключение
    """
    return {
        "error": {
            "code": code,
            "description": description,
        }
    }


class BaseApiException(Exception):
    """Ошибка запроса."""

    def __init__(
        self, *args: Any, response: Optional[Response] = None, **kwargs: Any
    ) -> None:
        """Инициализировать исключения в API."""
        if response is not None:
            self.response = response

        elif args and isinstance(args[0], Response):
            self.response = args[0]
            args = args[1:]

        super().__init__(*args, **kwargs)