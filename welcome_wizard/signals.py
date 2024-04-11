"""Signal handlers for welcome_wizard."""

from nautobot.extras.models import Job


def nautobot_database_ready_callback(sender, *, apps, **kwargs):  # pylint: disable=unused-argument
    """Callback function triggered by the nautobot_database_ready signal when the Nautobot database is fully ready."""
    jobs = ["WelcomeWizardImportManufacturer", "WelcomeWizardImportDeviceType"]

    for job_class in jobs:
        job = Job.objects.get(job_class_name=job_class)
        job.enabled = True
        job.save()
