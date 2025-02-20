"""Konstanten fuer die Viessmann PV GridX Integration."""

# Name der Integration
DOMAIN = "viessmann_pv"

CONF_USERNAME = "username"
CONF_PASSWORD = "password"
CONF_SCAN_INTERVAL = "scan_interval"

DEFAULT_SCAN_INTERVAL = 300  # Standardwert: 5 Minuten

# API-URLs
GRIDX_URLS = {
    "login": "https://gridx.eu.auth0.com/oauth/token",
    "gateways": "https://api.gridx.de/gateways",
    "live": "https://api.gridx.de/systems/{}/live"
}

# OAuth-Login-Daten (ohne Benutzerdaten)
GRIDX_LOGIN = {
    "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
    "audience": "my.gridx",
    "client_id": "oZpr934Ikn8OZOHTJEcrgXkjio0I0Q7b",
    "scope": "email openid",
    "realm": "viessmann-authentication-db"
}

# InfluxDB-Konfiguration
INFLUX_HOST = "localhost"  # Falls InfluxDB extern laeuft hier die IP anpassen
INFLUX_PORT = 8086
INFLUX_DATABASE = "iobroker"

# Standard-Aktualisierungsintervall (in Sekunden)
DEFAULT_UPDATE_INTERVAL = 60

# Logger-Name fuer das Debugging
LOGGER_NAME = "ViessmannPV"
