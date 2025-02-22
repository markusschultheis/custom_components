import aiohttp
import asyncio
import logging
from .const import AUTH_URL, GATEWAYS_URL, LIVE_URL

_LOGGER = logging.getLogger(__name__)

class GridXAPI:
    def __init__(self, username, password, client_id, realm, audience):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.realm = realm
        self.audience = audience
        self.token = None
        self.gateway_id = None

    async def authenticate(self):
        payload = {
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": self.username,
            "password": self.password,
            "audience": self.audience,
            "client_id": self.client_id,
            "scope": "email openid",
            "realm": self.realm
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(AUTH_URL, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                self.token = data.get("id_token")

                if response.status != 200:
                    _LOGGER.error(f"Authentifizuerung fehlgeschlagen: {response.status} - {data}")
                    raise Exception(f"Authentification failed: {response.status} - {data}")

    async def get_gateway_id(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(GATEWAYS_URL, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                self.gateway_id = data[0]["system"]["id"]

    async def get_live_data(self):
        headers = {"Authorization": f"Bearer {self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(LIVE_URL.format(self.gateway_id), headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data
