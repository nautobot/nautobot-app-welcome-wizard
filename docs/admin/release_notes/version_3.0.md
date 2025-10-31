# v3.0 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Introduces two new optional configuration parameters for manufacturer name transformation and mapping.
- Major internal refactor to adopt Nautobot v3’s NautobotUIViewSet and UI component structure.
- Upgraded to Bootstrap 5 and cleaned up legacy templates for compatibility with Nautobot v3.
- Dropped support for Python 3.8.

## [v3.0.0a1 (2025-10-31)](https://github.com/nautobot/nautobot-app-welcome-wizard/releases/tag/v3.0.0a1)

### Housekeeping

- [#122](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/122) - Changed model_class_name in .cookiecutter.json to a valid model to help with drift management.
- [#136](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/136) - Removed outdated html templates and cleaned up the view code to limit impact of Nautobot v3 and Bootstrap 5.
- [#137](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/137) - Add DJLint and DjHTML.
- [#139](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/139) - Bootstrap 5 Upgrade.
