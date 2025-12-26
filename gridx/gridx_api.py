import aiohttp
import logging
import time
from .const import (
    AUTH_URL,
    GATEWAYS_URL,
    LIVE_URL,
    GRANT_TYPE,
    DOMAIN,
    DATA_ID_TOKEN,
    DATA_EXPIRES_AT,
)

_LOGGER = logging.getLogger(__name__)

class GridXAPI:
    def __init__(self, hass, username, password, client_id, realm, audience):
        self.hass = hass
        self.username = username
        self.password = password
        self.client_id = client_id
        self.realm = realm
        self.audience = audience
        self.gateway_id = None
        self.id_token = None
                
    async def authenticate(self):
        """Fordert ein neues Token mit Benutzername und Passwort an."""
        payload = {
            "grant_type": GRANT_TYPE,
            "username": self.username,
            "password": self.password,
            "audience": self.audience,
            "client_id": self.client_id,
            "scope": "email openid offline_access",
            "realm": self.realm
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(AUTH_URL, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                self.id_token = data.get("id_token")
                self.hass.data[DOMAIN][DATA_ID_TOKEN] = self.id_token
                self.hass.data[DOMAIN][DATA_EXPIRES_AT] = data.get("expires_in") + time.time() - 52200

    async def get_gateway_id(self):
        headers = {"Authorization": f"Bearer {self.id_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(GATEWAYS_URL, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                self.gateway_id = data[0]["system"]["id"]

    async def get_live_data(self):
        now = time.time()

        if now > self.hass.data[DOMAIN][DATA_EXPIRES_AT]:
            _LOGGER.info("Token ist abgelaufen → authenticate() wird ausgeführt")
            await self.authenticate()

        headers = {"Authorization": f"Bearer {self.id_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(LIVE_URL.format(self.gateway_id), headers=headers) as response:
                response.raise_for_status()
                return await response.json()
