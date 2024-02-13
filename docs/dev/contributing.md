# Contributing to the App

The project is packaged with a light [development environment](dev_environment.md) based on `docker-compose` to help with the local development of the project and to run tests.

The project is following Network to Code software development guidelines and is leveraging the following:

- Python linting and formatting: `black`, `pylint`, `bandit`, `flake8`, and `ruff`.
- YAML linting is done with `yamllint`.
- Django unit test to ensure the app is working properly.

Documentation is built using [mkdocs](https://www.mkdocs.org/). The [Docker based development environment](dev_environment.md#docker-development-environment) automatically starts a container hosting a live version of the documentation website on [http://localhost:8001](http://localhost:8001) that auto-refreshes when you make any changes to your local files.

## Creating Changelog Fragments

All pull requests to `next` or `develop` must include a changelog fragment file in the `./changes` directory. To create a fragment, use your GitHub issue number and fragment type as the filename. For example, `2362.added`. Valid fragment types are `added`, `changed`, `deprecated`, `fixed`, `removed`, and `security`. The change summary is added to the file in plain text. Change summaries should be complete sentences, starting with a capital letter and ending with a period, and be in past tense. Each line of the change fragment will generate a single change entry in the release notes. Use multiple lines in the same file if your change needs to generate multiple release notes in the same category. If the change needs to create multiple entries in separate categories, create multiple files.

!!! example

    **Wrong**
    ```plaintext title="changes/1234.fixed"
    fix critical bug in documentation
    ```

    **Right**
    ```plaintext title="changes/1234.fixed"
    Fixed critical bug in documentation.
    ```

!!! example "Multiple Entry Example"

    This will generate 2 entries in the `fixed` category and one entry in the `changed` category.

    ```plaintext title="changes/1234.fixed"
    Fixed critical bug in documentation.
    Fixed release notes generation.
    ```

    ```plaintext title="changes/1234.changed"
    Changed release notes generation.
    ```

## Branching Policy

Nautobot Welcome Wizard follows the GitHub Flow with Develop being the source branch for contribution branches. Please create a fork of the repo and submit your PR to the Develop branch.

## Submitting Pull Requests

- It is recommended to open an issue **before** starting work on a pull request, and discuss your idea with the Nautobot maintainers before beginning work. This will help prevent wasting time on something that we might not be able to implement. When suggesting a new feature, also make sure it won't conflict with any work that's already in progress.

- Once you've opened or identified an issue you'd like to work on, ask that it
  be assigned to you so that others are aware it's being worked on. A maintainer
  will then mark the issue as "accepted."

- If you followed the project guidelines, have ample tests, code quality, you will first be acknowledged for your work. So, thank you in advance! After that, the PR will be quickly reviewed to ensure that it makes sense as a contribution to the project, and to gauge the work effort or issues with merging into *current*. If the effort required by the core team isn’t trivial, it’ll likely still be a few weeks before it gets thoroughly reviewed and merged, thus it won't be uncommon to move it to *near term* with a `near-term` label. It will just depend on the current backlog.

- All code submissions should meet the following criteria (CI will enforce
these checks):
  - Python syntax is valid
  - All unit tests pass successfully
  - PEP 8 compliance is enforced, with the exception that lines may be
    greater than 80 characters in length

## Release Policy

Maintainers with write access to the repo will be able to create a new release. We follow [SemVer](https://semver.org) for our versioning.

Please follow the [Release Checklist](release_checklist.md) when creating a release.
