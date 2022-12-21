# Uninstall the App from Nautobot

Here you will find any steps necessary to cleanly remove the App from your Nautobot environment.

## Uninstall Guide

Here is the removal process for Welcome Wizard.

## Database Cleanup

Revert the database migrations for Welcome Wizard:

```shell
nautobot-server migrate welcome_wizard zero
```

Remove the configuration you added in `nautobot_config.py` from `PLUGINS` & `PLUGINS_CONFIG`.

Drop all tables from the plugin: `nautobot_plugin_welcome_wizard*` if they exist.
