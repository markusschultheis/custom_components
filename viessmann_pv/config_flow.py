import logging
import voluptuous as vol
from homeassistant import config_entries, core, exceptions
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from .const import DOMAIN, GRIDX_URLS
import requests

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required("username"): str,
    vol.Required("password"): str,
    vol.Required("client_id"): str,
})

def validate_input(data: dict) -> bool:
    """Validate credentials against the GridX API."""
    auth_data = {
        "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
        "username": data["username"],
        "password": data["password"],
        "audience": "my.gridx",
        "client_id": data["client_id"],
        "scope": "email openid",
        "realm": "viessmann-authentication-db",
    }
    response = requests.post(GRIDX_URLS["login"], json=auth_data)
    
    if response.status_code == 200:
        return True
    else:
        _LOGGER.error("Authentication failed: %s", response.text)
        raise InvalidAuth

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for GridX PV integration."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            try:
                if await self.hass.async_add_executor_job(validate_input, user_input):
                    return self.async_create_entry(title="GridX PV", data=user_input)
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"

        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

class InvalidAuth(exceptions.HomeAssistantError):
    """Error to indicate invalid authentication."""
