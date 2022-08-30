"""Platform for switch integration."""
from __future__ import annotations

import logging
import socket
import json
import voluptuous as vol

# Import the device class from the component that you want to support
import homeassistant.helpers.config_validation as cv
from homeassistant.components.switch import (PLATFORM_SCHEMA, SwitchEntity)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

DOMAIN = "ali_ip_relay"

_LOGGER = logging.getLogger(__name__)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required('ip'): cv.string,
    vol.Required('port', default=1234): cv.port
})


def setup_platform(
    hass: HomeAssistant,
    config: ConfigType,
    add_entities: AddEntitiesCallback,
    discovery_info: DiscoveryInfoType | None = None
) -> None:
    """Set up the Awesome Light platform."""
    # Assign configuration variables.
    # The configuration check takes care they are present.
    ip = config['ip']
    port = config['port']
    # Setup connection with devices/cloud
    sock = socket.socket()
    sock.connect((str(ip), port))
    sock.send('state=?'.encode())
    data = sock.recv(1024)
    sock.close()
    if not data:
        _LOGGER.error("Could not connect to ali_ip_relay hub")
        return
    data = data.decode()
    if not data:
        _LOGGER.error("Could not connect to ali_ip_relay hub")
        return
    data = json.loads(data)
    if not data:
        _LOGGER.error("Could not connect to ali_ip_relay hub")
        return
    if data['cmd'] != 'state':
        _LOGGER.error("Could not connect to ali_ip_relay hub")
        return

    sn = data['sn']
    runtime = data['runtime']
    # Add devices
    add_entities(ali_ip_relay(ip, port, sn, i + 1,
                 data['output'][i]) for i in range(0, len(data['output'])))


class ali_ip_relay(SwitchEntity):

    def __init__(self, ip, port, sn, num, state) -> None:
        """Initialize an AwesomeLight."""
        self._ip = ip
        self._port = port
        self._sn = sn
        self._num = num
        self._id = sn + '_' + str(num)
        self._name = 'ali_ip_relay_' + sn + '_' + str(num)
        self._state = True if state == '1' else False
        # hass.states.set(DOMAIN + '.' + self._id + '.test', self._sn)

    @ property
    def name(self) -> str:
        """Return the display name of this light."""
        return self._name

    @ property
    def is_on(self) -> bool | None:
        """Return true if light is on."""
        return self._state

    def turn_on(self, **kwargs: Any) -> None:
        """Instruct the light to turn on.
        You can skip the brightness part if your light does not support
        brightness control.
        """
        pass

    def turn_off(self, **kwargs: Any) -> None:
        """Instruct the light to turn off."""
        pass

    def toggle(self, **kwargs):
        """Toggle the entity."""
        pass

    def update(self) -> None:
        """Fetch new state data for this light.
        This is the only method that should fetch new data for Home Assistant.
        """

        pass
