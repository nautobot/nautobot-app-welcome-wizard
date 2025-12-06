# v2.2 Release Notes

This document describes all new features and changes in the release. The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Release Overview

- Changed minimum Nautobot version to 2.4.20.
- Dropped support for Python versions 3.8 and 3.9.

<!-- towncrier release notes start -->
## [v2.2.0 (2025-12-05)](https://github.com/nautobot/nautobot-app-welcome-wizard/releases/tag/v2.2.0)

### Added

- [#129](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/129) - Added two new optional configurations to be used in `nautobot_config.py` for enabling Manufacturer name transformations: `manufacturer_transform_func` and `manufacturer_map`.

### Fixed

- [#127](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/127) - Fixed issue with `ModuleBayTemplate` components not being created when importing DeviceTypes.

### Dependencies

- [#130](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/130) - Pinned Django debug toolbar to ~5.2.0.

### Housekeeping

- [#122](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/122) - Changed model_class_name in .cookiecutter.json to a valid model to help with drift management.
- [#136](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/136) - Removed outdated html templates and cleaned up the view code to limit impact of Nautobot v3 and Bootstrap 5.
- [#137](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/137) - Added DJLint and DjHTML.
- [#381](https://github.com/nautobot/nautobot-app-welcome-wizard/issues/381) - Refactored to use NautobotUIViewSet and UI components.
- Rebaked from the cookie `nautobot-app-v2.4.1`.
- Rebaked from the cookie `nautobot-app-v2.4.2`.
- Rebaked from the cookie `nautobot-app-v2.5.0`.
- Rebaked from the cookie `nautobot-app-v2.5.1`.
- Rebaked from the cookie `nautobot-app-v2.6.0`.
- Rebaked from the cookie `nautobot-app-v2.7.0`.
- Rebaked from the cookie `nautobot-app-v2.7.1`.
- Rebaked from the cookie `nautobot-app-v2.7.2`.
