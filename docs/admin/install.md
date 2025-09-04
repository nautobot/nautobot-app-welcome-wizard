# Installing the App in Nautobot

Here you will find detailed instructions on how to **install** and **configure** the App within your Nautobot environment.

## Prerequisites

- The app is compatible with Nautobot 2.0.0 and higher.
- Databases supported: PostgreSQL, MySQL

!!! note
    Please check the [dedicated page](compatibility_matrix.md) for a full compatibility matrix and the deprecation policy.

## Install Guide

!!! note
    Apps can be installed from the [Python Package Index](https://pypi.org/) or locally. See the [Nautobot documentation](https://docs.nautobot.com/projects/core/en/stable/user-guide/administration/installation/app-install/) for more details. The pip package name for this app is [`nautobot-welcome-wizard`](https://pypi.org/project/nautobot-welcome-wizard/).

The app is available as a Python package via PyPI and can be installed with `pip`:

```shell
pip install nautobot-welcome-wizard
```

To ensure Welcome Wizard is automatically re-installed during future upgrades, create a file named `local_requirements.txt` (if not already existing) in the Nautobot root directory (alongside `requirements.txt`) and list the `nautobot-welcome-wizard` package:

```shell
echo nautobot-welcome-wizard >> local_requirements.txt
```

Once installed, the app needs to be enabled in your Nautobot configuration. The following block of code below shows the additional configuration required to be added to your `nautobot_config.py` file:

- Append `"welcome_wizard"` to the `PLUGINS` list.
- Append the `"welcome_wizard"` dictionary to the `PLUGINS_CONFIG` dictionary and override any defaults.

```python
# In your nautobot_config.py
PLUGINS = ["welcome_wizard"]

# PLUGINS_CONFIG = {
#   "welcome_wizard": {
#     "enable_devicetype-library": True,
#     "enable_welcome_banner": True,
#     "manufacturer_uppercase": False,
#     "manufacturer_map": {},
#   }
# }
```

`manufacturer_uppercase` transformation can also be configured using `$WELCOME_WIZARD_MANUFACTURER_UPPERCASE` environment variable (which can be set to a string that can be converted to `True` or `False` using Nautobot's `is_truthy()` function), examples: `true`, `True`, `y`, `yes`, `on`, `1`.

Once the Nautobot configuration is updated, run the Post Upgrade command (`nautobot-server post_upgrade`) to run migrations and clear any cache:

```shell
nautobot-server post_upgrade
```

Then restart (if necessary) the Nautobot services which may include:

- Nautobot
- Nautobot Workers
- Nautobot Scheduler

```shell
sudo systemctl restart nautobot nautobot-worker nautobot-scheduler
```

## App Configuration

The app behavior can be controlled with the following list of settings:

| Key     | Example | Default | Description                          |
| ------- | ------ | -------- | ------------------------------------- |
| `enable_devicetype-library` | `True` | `True` | If enabled, the [device type](https://github.com/nautobot/devicetype-library) git repository will be automatically added for you. |
| `enable_welcome_banner` | `True` | `True` | If enabled, the Welcome Wizard banner will display on the home screen for authenticated users. |
| `manufacturer_uppercase` | `True` | `False` | If enabled, all Manufacturer names will be converted to upper case. |
| `manufacturer_map` | `{"Arista": "Arista Networks", "Cisco": "Cisco Systems"}` | `{}` | If dictionary is defined, all manufacturer names matching its keys will be transformed to corresponding mapping values. |
