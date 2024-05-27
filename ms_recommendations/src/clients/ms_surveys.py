"""
Функции для взаимодействия с внешним сервисом-провайдером данных о местонахождении.
"""
from http import HTTPStatus
from typing import Optional
from urllib.parse import urlencode, urljoin

import httpx


class LocationClient:
    """
    Реализация функций для взаимодействия с внешним сервисом-провайдером данных о местонахождении.
    """

    def __init__(self, headers = None, cookies = None):
        self.url = 'http://ms_surveys/api/v1/'
        self.headers = headers
        self.cookies = cookies

    async def _request(self, url: str) -> Optional[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, cookies=self.cookies)
            if response.status_code == HTTPStatus.OK:
                return response.json()

            return None


    async def get_surveys(self, ids: list[str]) -> Optional[dict]:
        """
        Получение данных об опросах по списку идентификаторов
        """

        url = urljoin(self.base_url, "surveys/pick",)
        return await self._request(url)