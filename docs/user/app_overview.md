# App Overview

This document provides an overview of the App including critical information and import considerations when applying it to your Nautobot environment.

!!! note
    Throughout this documentation, the terms "app" and "plugin" will be used interchangeably.

## Description

The Welcome Wizard is an open-source Nautobot plugin with the goal to assist users with the necessary initial steps in populating data within Nautobot.

The Welcome Wizard adds four (4) key features:

- Welcome Wizard uses the **Import Wizard** to allow ease of adding community-defined Device Types and Manufacturers into Nautobot. This is built upon the Git datasources feature of Nautobot.
- Welcome Wizard includes by default the **[DeviceType-library](https://github.com/netbox-community/devicetype-library)**, but this can be disabled and a custom library can be used instead.
- Welcome Wizard includes **banners** in forms to alert the user when required form fields have no associated resources in Nautobot.
- The Welcome Wizard **Dashboard** contains a list of common Nautobot Data Models that many other Nautobot models require. This page allows ease of adding items to Nautobot or, if supported, importing them.


## Audience (User Personas) - Who should use this App?

Anyone building a new instance of Nautobot who struggles with where to start when faced with an empty database. You might try to add a Device, only to find that you need to create a Device Type, Site, and Device Role. You go to add a Device Type and find you need a Manufacturer (which is not directly required for a Device). This app tries to alleviate some of these problems.

## Authors and Maintainers

!!! warning "Developer Note - Remove Me!"
    Add the team and/or the main individuals maintaining this project. Include historical maintainers as well.

## Nautobot Features Used

Welcome Wizard helps you import the following data types:

- Sites
- Manufacturers
- Device Types
- Device Roles
- Circuit Types
- Circuit Providers
- RIRs
- VM Cluster Types
