# Using the App

This document describes common use-cases and scenarios for this App.

## General Usage

The Nautobot Welcome Wizard includes a great dashboard to help you get started with Nautobot. One annoyance when using Nautobot is finding item dependencies only after you've filled out half a form. For example, when creating a `device` only to find out you need a `device type`. Then discovering you also need a manufacturer when trying to create the `device type`.

### The Dashboard

This is where the Welcome Wizard Dashboard will help. It is a single location you can visit to find links to common dependencies. If a resource in Nautobot requires another it will be listed here. The `Name` column includes links to view a list of the associated resources. The `Completed` column will show if a resource has been created. The `Ignored` column allows the administrator (through the admin panel) tp mark a dependency as ignored if that resource that will be unused. Finally, the `Actions` column will have two button links. The first is a green plus which will take you to the resource creation form. The blue wizard hat will take you to the [Import Wizard](app_getting_started.md#import-manufacturers) allowing you to import from a git repository.

![Welcome Wizard](../images/welcome_wizard.png)

#### Completed Column

The Welcome Wizard automatically tracks the resources in Nautobot. For instance, once you add a `Site` to Nautobot,
the column will update (upon page reload) to show as completed.

![Dashboard with Completions](../images/dashboard_with_completions.png)

#### Ignored Column

Tracking fields that are ignored is done through the Nautobot Admin Panel. Head over to the user menu (top-right), then into the admin panel, and navigate to `Merlin` under the `Nautobot Welcome Wizard` heading.

![Navigate to Merlin](../images/merlin_admin_navigation.png)

Next choose the `Merlin` field you would like to change. You can click on the Name field to edit.

![Select Merlin Field](../images/merlin_admin_selection.png)

Once selected, check the `Ignored` checkbox and then `Save`. In the example below, we are ignoring the RIRs.

![Ignored Field](../images/merlin_admin_ignored.png)

Navigate back to the Getting Started Dashboard to see that your field is marked as ignored.

![Ignored Dashboard](../images/dashboard_with_ignored.png)

### Middleware

The Welcome Wizard App comes packed with helpful middleware.

#### Homepage Banner

Upon loading the Nautobot Homepage, the Nautobot Welcome Wizard greets you with a message to help guide you to the dashboard.

![Welcome Wizard Banner](../images/merlin_banner.png)

#### Required Fields

The Welcome Wizard checks any Nautobot form for required fields. If a field is required and does not have at least one resource created for that field, it will add a message to the top of the page with a link to add the resource.

![Middleware message x1](../images/merlin_middleware_import.png)

If multiple required fields have missing resources you will get a message for each missing item.

![Middleware message x3](../images/merlin_middleware_x3.png)


## Use-cases and common workflows

For adding community defined Device Types and Manufacturers into Nautobot, check out the [Import Wizard](app_getting_started.md#import-manufacturers).

Welcome Wizard includes settings that are enabled by default to ease the user in setting up and syncing from a [Git Repository Data Source](git_datasource.md).


## Screenshots

### Welcome Wizard Banner

![Welcome Wizard Banner](../images/merlin_banner.png)

### Welcome Wizard Middleware

![Welcome Wizard Middleware](../images/merlin_middleware_x3.png)

### Welcome Wizard Dashboard

![Welcome Wizard Dashboard](../images/welcome_wizard.png)

### Welcome Wizard Completions

![Welcome Wizard Completions](../images/dashboard_with_completions.png)

### Welcome Wizard Import Device Types

![Welcome Wizard Import Device Types](../images/merlin_import_device_type.png)
