import aiohttp
import logging
import time
from .const import AUTH_URL, GATEWAYS_URL, LIVE_URL, GRANT_TYPE

_LOGGER = logging.getLogger(__name__)

class GridXAPI:
    def __init__(self, username, password, client_id, realm, audience):
        self.username = username
        self.password = password
        self.client_id = client_id
        self.realm = realm
        self.audience = audience
        self.token_expires_at = 0
        self.access_token = None
        self.refresh_token = None
        self.gateway_id = None
        self.id_token = None
        _LOGGER.info(f"{GridXAPI}")

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
        _LOGGER.info(f"{payload}")

        async with aiohttp.ClientSession() as session:
            async with session.post(AUTH_URL, json=payload) as response:
                response.raise_for_status()
                data = await response.json()
                _LOGGER.info(f"{data}")
                self.access_token = data.get("access_token")
                self.id_token = data.get("id_token")
                self.refresh_token = data.get("refresh_token")  # Speichert das Refresh-Token
                expires_in = data.get("expires_in", 3600)
                self.token_expires_at = time.time() + expires_in

                _LOGGER.info(f"Neues Access Token erhalten, gültig bis: {time.ctime(self.token_expires_at)}")

    async def refresh_access_token(self):
        """Erneuert das Token mit dem gespeicherten Refresh-Token."""
        if not self.refresh_token:
            _LOGGER.warning("Kein Refresh-Token vorhanden. Authentifiziere neu...")
            await self.authenticate()
            return

        payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(AUTH_URL, json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    self.id_token = data.get("id_token")
                    expires_in = data.get("expires_in", 3600)
                    self.token_expires_at = time.time() + expires_in

                    _LOGGER.info(f"Access Token erneuert, gültig bis: {self.token_expires_at}")
                else:
                    _LOGGER.warning(f"Token-Erneuerung fehlgeschlagen ({response.status}). Erneute Authentifizierung...")
                    await self.authenticate()  # Fallback: Komplett neu authentifizieren

    def is_token_valid(self):
        """Prüft, ob das gespeicherte Token noch gültig ist."""
        return self.id_token is not None and time.time() < self.token_expires_at

    async def get_valid_token(self):
        """Stellt sicher, dass ein gültiges Token vorhanden ist."""
        if not self.is_token_valid():
            _LOGGER.info("Token abgelaufen oder nicht vorhanden. Versuche zu erneuern...")
            await self.refresh_access_token()
        return self.id_token

    async def get_gateway_id(self):
        id_token = await self.get_valid_token()
        headers = {"Authorization": f"Bearer {id_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(GATEWAYS_URL, headers=headers) as response:
                response.raise_for_status()
                data = await response.json()
                self.gateway_id = data[0]["system"]["id"]

    async def get_live_data(self):
        id_token = await self.get_valid_token()
        headers = {"Authorization": f"Bearer {id_token}"}
        async with aiohttp.ClientSession() as session:
            async with session.get(LIVE_URL.format(self.gateway_id), headers=headers) as response:
                response.raise_for_status()
                return await response.json()
