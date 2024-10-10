# Welcome Wizard

<p align="center">
  <img src="https://raw.githubusercontent.com/nautobot/nautobot-app-welcome-wizard/develop/docs/images/icon-nautobot-welcome-wizard.svg" class="logo" height="200px">
  <br>
  <a href="https://github.com/nautobot/nautobot-app-welcome-wizard/actions"><img src="https://github.com/nautobot/nautobot-app-welcome-wizard/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="https://docs.nautobot.com/projects/welcome-wizard/en/latest/"><img src="https://readthedocs.org/projects/nautobot-plugin-welcome-wizard/badge/"></a>
  <a href="https://pypi.org/project/nautobot-welcome-wizard/"><img src="https://img.shields.io/pypi/v/nautobot-welcome-wizard"></a>
  <a href="https://pypi.org/project/nautobot-welcome-wizard/"><img src="https://img.shields.io/pypi/dm/nautobot-welcome-wizard"></a>
  <br>
  An <a href="https://networktocode.com/nautobot-apps/">App</a> for <a href="https://nautobot.com/">Nautobot</a>.
</p>

## Overview

### What is the Nautobot Welcome Wizard?

The Welcome Wizard is a getting started wizard for [Nautobot](https://docs.nautobot.com/projects/core/en/stable/) to assist a new user with necessary initial steps in populating data.

![Welcome Wizard GIF](https://raw.githubusercontent.com/nautobot/nautobot-app-welcome-wizard/develop/docs/images/WelcomeWizard.gif)

## Key Features

The Welcome Wizard adds four (4) key features:

1. [**Import Wizard**](https://docs.nautobot.com/projects/welcome-wizard/en/latest/user/app_getting_started/#import-manufacturers) - Welcome Wizard uses the `Import Wizard` to allow ease of adding community defined Device Types and Manufacturers into Nautobot.

2. [**Quick-Start Settings**](https://docs.nautobot.com/projects/welcome-wizard/en/latest/user/git_datasource/) - Welcome Wizard includes settings that are enabled by default to ease the user in setting up and syncing from a Git Repository.

3. [**Helpful Middleware**](https://docs.nautobot.com/projects/welcome-wizard/en/latest/user/app_use_cases/#middleware) - Welcome Wizard includes middleware banners to assist with Nautobot resource creation.

4. [**Dashboard**](https://docs.nautobot.com/projects/welcome-wizard/en/latest/user/app_use_cases/) - The Welcome Wizard Dashboard contains a list of common Nautobot Data Models that many other Nautobot models require. This page allows ease of adding items to Nautobot or, if supported, importing them. This ties all of the features together.

### Screenshots

More screenshots can be found in the [Using the App](https://docs.nautobot.com/projects/welcome-wizard/en/latest/user/app_use_cases/) page in the documentation. Here's a quick overview of some of the app's added functionality:

![Welcome Wizard Banner](https://raw.githubusercontent.com/nautobot/nautobot-app-welcome-wizard/develop/docs/images/merlin_banner.png)

![Welcome Wizard Middleware](https://raw.githubusercontent.com/nautobot/nautobot-app-welcome-wizard/develop/docs/images/merlin_middleware_x3.png)

![Welcome Wizard Dashboard](https://raw.githubusercontent.com/nautobot/nautobot-app-welcome-wizard/develop/docs/images/welcome_wizard.png)

![Welcome Wizard Completions](https://raw.githubusercontent.com/nautobot/nautobot-app-welcome-wizard/develop/docs/images/dashboard_with_completions.png)

![Welcome Wizard Import Device Types](https://raw.githubusercontent.com/nautobot/nautobot-app-welcome-wizard/develop/docs/images/merlin_import_device_type.png)

## Documentation

Full documentation for this App can be found over on the [Nautobot Docs](https://docs.nautobot.com) website:

- [User Guide](https://docs.nautobot.com/projects/welcome-wizard/en/latest/user/app_overview/) - Overview, Using the App, Getting Started.
- [Administrator Guide](https://docs.nautobot.com/projects/welcome-wizard/en/latest/admin/install/) - How to Install, Configure, Upgrade, or Uninstall the App.
- [Developer Guide](https://docs.nautobot.com/projects/welcome-wizard/en/latest/dev/contributing/) - Extending the App, Code Reference, Contribution Guide.
- [Release Notes / Changelog](https://docs.nautobot.com/projects/welcome-wizard/en/latest/admin/release_notes/).
- [Frequently Asked Questions](https://docs.nautobot.com/projects/welcome-wizard/en/latest/user/faq/).

### Contributing to the Documentation

You can find all the Markdown source for the App documentation under the [`docs`](https://github.com/nautobot/nautobot-app-welcome-wizard/tree/develop/docs) folder in this repository. For simple edits, a Markdown capable editor is sufficient: clone the repository and edit away.

If you need to view the fully-generated documentation site, you can build it with [MkDocs](https://www.mkdocs.org/). A container hosting the documentation can be started using the `invoke` commands (details in the [Development Environment Guide](https://docs.nautobot.com/projects/welcome-wizard/en/latest/dev/dev_environment/#docker-development-environment)) on [http://localhost:8001](http://localhost:8001). Using this container, as your changes to the documentation are saved, they will be automatically rebuilt and any pages currently being viewed will be reloaded in your browser.

Any PRs with fixes or improvements are very welcome!

## Questions

For any questions or comments, please check the [FAQ](https://docs.nautobot.com/projects/welcome-wizard/en/latest/user/faq/) first. Feel free to also swing by the [Network to Code Slack](https://networktocode.slack.com/) (channel `#nautobot`), sign up [here](http://slack.networktocode.com/) if you don't have an account.
