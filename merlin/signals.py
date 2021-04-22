"""Post Migrate Merlin Script."""

from django.conf import settings


def merlin_devicetype(apps, **kwargs):
    """Add a git repository if enabled in settings."""
    git_repository = apps.get_model("extras", "GitRepository")
    if settings.PLUGINS_CONFIG["merlin"].get("enable_devicetype-library"):
        try:
            repo = git_repository.objects.get(name="Devicetype-library")
        except git_repository.DoesNotExist:
            repo = git_repository(
                name="Devicetype-library",
                slug="devicetype_library",
                remote_url="https://github.com/netbox-community/devicetype-library.git",
                provided_contents=[
                    "merlin.device_type_importer",
                ],
                branch="master",
            )
            print(repo)
            repo.save(trigger_resync=False)
