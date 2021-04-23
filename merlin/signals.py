"""Post Migrate Merlin Script."""

from django.conf import settings


def merlin_devicetype(apps, **kwargs):
    """Add a git repository if enabled in settings."""
    git_repository = apps.get_model("extras", "GitRepository")
    if settings.PLUGINS_CONFIG["merlin"].get("enable_devicetype-library"):
        git_repository.objects.update_or_create(
            name="Devicetype-library",
            slug="devicetype_library",
            remote_url="https://github.com/netbox-community/devicetype-library.git",
            provided_contents=[
                "merlin.import_wizard",
            ],
            branch="master",
        )
