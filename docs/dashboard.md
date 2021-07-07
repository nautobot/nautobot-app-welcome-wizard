# Getting Started Dashboard

The Nautobot Welcome Wizard includes a great dashboard to help you get started with Nautobot. One annoyance when using Nautobot, is finding that when say, creating a `device`, you fill out half the form only to find out you need a `device type`.  You then find when trying to create the `device type` that you also need a manufacturer.

## The Dashboard

This is where the Getting Started Dashboard will help. It is a single location that you can visit to find links to common dependencies. If a resource in Nautobot requires another, it will be listed here. The `Name` column includes links to view a list of the associated resources. The `Completed` column will show if a resource has been created. The `Ignored` column allows the administrator (through the admin panel) mark a dependency as ignored if that is a resource that will be unused. Finally, the `Actions` column will have two button links. The first is the green plus which will take you to the resource creation form. The blue wizard hat will take you to the [Import Wizard](import_wizard.md) allowing you to import from a git repository.

![Getting Started Dashboard](./img/getting_started_dashboard.png)

### Completed Column

The Welcome Wizard automatically tracks the resources in Nautobot.  For instance, once you add a `Site` to Nautobot,
the column will update (upon page reload) to show completed.

![Dashboard with Completions](./img/getting_started_dashboard_with_completions.png)

### Ignored Column

Tracking fields that are ignored are done through the Django Admin Panel. Log into the admin panel and navigate to `Merlin`.

![Navigate to Merlin](./img/Merlin_admin_navigation.png)

Next you will choose the `Merlin` field you would like to change. You can click on the Name field to edit.

![Select Merlin Field](./img/merlin_admin_selection.png)

Once selected, you will check the `Ignored` checkbox and then `Save`. In the example below, we are ignoring the RIRs.

![Ignored Field](./img/merlin_admin_ignored.png)

Navigate back to the Getting Started Dashboard, you will now see that your field is marked as ignored.

![Ignored Dashboard](./img/getting_started_dashboard_with_ignored.png)