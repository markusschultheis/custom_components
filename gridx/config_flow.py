from homeassistant import config_entries
import voluptuous as vol
from .const import DOMAIN, CONF_CLIENT_ID, CONF_REALM, CONF_AUDIENCE

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Viessmann PV-Anlage."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(title="Viessmann PV-Anlage", data=user_input)

        schema = vol.Schema({
            vol.Required("username"): str,
            vol.Required("password"): str,
            vol.Required(CONF_CLIENT_ID, default="mG0Phmo7DmnvAqO7p6B0WOYBODppY3cc"): str,
            vol.Required(CONF_REALM, default="eon-home-authentication-db"): str,
            vol.Required(CONF_AUDIENCE, default="my.gridx"): str,
        })

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)
