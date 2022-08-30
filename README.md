# ali_ip_relay

This integration shows how you would go ahead and integrate a physical light into Home Assistant.

If you use this integration as a template, make sure you tweak the following places:

 - `manifest.json`: update the requirements to point at your Python library
 - `switch.py`: update the code to interact with your library

### Installation

Copy this folder to `<config_dir>/custom_components/ali_ip_relay/`.

Add the following entry in your `configuration.yaml`:

```yaml
switch:
  - platform: ali_ip_relay
    ip: IP_HERE
    port: PORT_HERE
```
