![Merlin](img/Merlin.svg "Merlin logo")

# What is Merlin?

Merlin is a getting started for wizard for [Nautobot](https://nautobot.readthedocs.io/en/latest/) to assist a new user with necessary initial steps in populating data.  

## Key Use Cases

Merlin enables three (3) key use cases:  

1. **Dashboard for Common Usecases** - Nautobot core data models are used to define the intended state of network infrastructure enabling it as a Source of Truth. While a baseline set of models are provided (such as IP networks and addresses, devices and racks, circuits and cable, etc.) it is Nautobot's goal to offer maximum data model flexibility. This is enabled through features such as user-defined relationships, custom fields on any model, and data validation that permits users to codify everything from naming standards to having automated tests run before data can be populated into Nautobot.

2. **Import Wizard** - Merlin uses the `Import Wizard` to allow ease of adding Device Types and Manufacturers into Nautobot.

3. **Quickstart Settings** - Merlin includes settings that are enabled by default to ease the user in setting up and syncing from a GitRepository.

## Design Philosophy

The following tenets drive the direction of Nautobot.

### Replicate the Real World

Careful consideration has been given to the data model to ensure that it can accurately reflect a real-world network. For instance, IP addresses are assigned not to devices, but to specific interfaces attached to a device, and an interface may have multiple IP addresses assigned to it.

### Serve as a Source of Truth (SoT)

Nautobot intends to represent the _desired_ state of a network versus its _operational_ state. While plugins and apps can be built and integrated with Nautobot to extend its capabilities to various aspects of the _operational_ state, the core platform's focus is on the _desired_ state.

### Serve as a Network Automation Platform

Nautobot intends to be a vehicle to deliver high-value network automation apps.  Using the extensible plugin system, users have the choice and freedom to create the integrations that make sense for them.

### Ensure Maximum Flexibility & Extensibility

While Nautobot intends to replicate the real world and offer opinionated models to get started defining the intended state of the network, it is understood that organizations and networks have unique design considerations that may need to be addressed in the SoT or Network Automation Platform.  Nautobot strives to enable flexibility and extensibility to power and automate all types of networks.

### Keep it Simple

When given a choice between a relatively simple [80% solution](https://en.wikipedia.org/wiki/Pareto_principle) and a much more complex complete solution, the former will typically be favored. This ensures a lean codebase with a low learning curve.

## Supported Python Versions

Merlin supports Python 3.6, 3.7, and 3.8.

## Getting Started

See the [installation guide](installation/index.md) for help getting Nautobot up and running quickly.
