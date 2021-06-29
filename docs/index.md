![Merlin](img/Merlin.svg "Merlin logo")

# What is the Nautobot Welcome Wizard?

The Welcome Wizard is a getting started wizard for [Nautobot](https://nautobot.readthedocs.io/en/latest/) to assist a new user with necessary initial steps in populating data.  

## Key Features

The Welcome Wizard add three (3) key features:  

1. **Dashboard for Common Usecases** - Nautobot core data models are used to define the intended state of network infrastructure enabling it as a Source of Truth. While a baseline set of models are provided (such as IP networks and addresses, devices and racks, circuits and cable, etc.) it is Nautobot's goal to offer maximum data model flexibility. This is enabled through features such as user-defined relationships, custom fields on any model, and data validation that permits users to codify everything from naming standards to having automated tests run before data can be populated into Nautobot.

2. **Import Wizard** - Welcome Wizard uses the `Import Wizard` to allow ease of adding Device Types and Manufacturers into Nautobot.

3. **Quickstart Settings** - Welcome Wizard includes settings that are enabled by default to ease the user in setting up and syncing from a GitRepository.

## Design Philosophy

The following tenets drive the direction of Welcome Wizard.

### Keep it Simple

When given a choice between a relatively simple [80% solution](https://en.wikipedia.org/wiki/Pareto_principle) and a much more complex complete solution, the former will typically be favored. This ensures a lean codebase with a low learning curve.

## Supported Python Versions

Welcome Wizard supports Python 3.6, 3.7, and 3.8.
