import aiohttp
import asyncio
import logging
import time
from .const import AUTH_URL, GATEWAYS_URL, LIVE_URL

_LOGGER = logging.getLogger(__name__)

class GridXAPI:
    def __init__(self, username, password, client_id, realm, audience):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.realm = realm
        self.audience = audience
        self.expires_at = 0
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
                expires_in = data.get("expires_in", 3600)
                self.expires_at = time.time() + expires_in
                
                _LOGGER.info("Authentifizierung erfolgreich. Token gueltig bis s%:", self.expires_at)

                if response.status != 200:
                    _LOGGER.error(f"Authentifizuerung fehlgeschlagen: {response.status} - {data}")
                    raise Exception(f"Authentification failed: {response.status} - {data}")

    def is_token_valid(self):
        """Prüft, ob das gespeicherte Token noch gültig ist."""
        return self.token is not None and time.time() < self.expires_at

    async def get_valid_token(self):
        """Stellt sicher, dass ein gültiges Token vorhanden ist."""
        if not self.is_token_valid():
            _LOGGER.info("Token ist abgelaufen oder nicht vorhanden. Authentifiziere erneut...")
            await self.authenticate()
        return self.token
        
    async def get_gateway_id(self):
        access_token = await self.get_valid_token() 
        headers = {"Authorization": f"Bearer {self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(GATEWAYS_URL, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                self.gateway_id = data[0]["system"]["id"]

    async def get_live_data(self):
        access_token = await self.get_valid_token() 
        headers = {"Authorization": f"Bearer {self.token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(LIVE_URL.format(self.gateway_id), headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                return data
