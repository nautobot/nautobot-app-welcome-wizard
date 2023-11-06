"""Tests for Welcome Wizard Datasources."""
import os
import tempfile
import uuid
from unittest import mock

import yaml
from django.contrib.auth import get_user_model
from django.test import RequestFactory
from nautobot.core.jobs import GitRepositorySync
from nautobot.core.testing import TransactionTestCase, run_job_for_testing
from nautobot.extras.choices import JobResultStatusChoices

# from nautobot.extras.datasources.git import enqueue_pull_git_repository_and_refresh_data
from nautobot.extras.datasources.registry import get_datasource_contents
from nautobot.extras.models import GitRepository, JobResult

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport

# Use the proper swappable User model
User = get_user_model()


@mock.patch("nautobot.extras.datasources.git.GitRepo")
class GitTest(TransactionTestCase):
    """Git Tests."""

    databases = ("default", "job_logs")

    COMMIT_HEXSHA = "88dd9cd78df89e887ee90a1d209a3e9a04e8c841"

    def setUp(self):
        """Setup tests."""
        super().setUp()

        self.user = User.objects.create_user(username="testuser")
        self.factory = RequestFactory()
        self.dummy_request = self.factory.get("/no-op/")
        self.dummy_request.user = self.user
        # Needed for use with the change_logging decorator
        self.dummy_request.id = uuid.uuid4()

        self.repo = GitRepository(
            name="Test Git Repository",
            slug="test_git_repo",
            remote_url="http://localhost/git.git",
            # Provide everything we know we can provide
            provided_contents=[entry.content_identifier for entry in get_datasource_contents("extras.gitrepository")],
        )
        self.repo.save()

        self.job_result = JobResult.objects.create(name=self.repo.name)

    def test_pull_git_repository_and_refresh_data_with_valid_data(self, mock_git_repo):
        """The test_pull_git_repository_and_refresh_data job should succeed if valid data is present in the repo."""
        # with tempfile.TemporaryDirectory() as tempdir:
        #     with self.settings(GIT_ROOT=tempdir):

        #         def populate_repo(path, _url):
        #             os.makedirs(path)
        #             # Load device-types data for git-repository
        #             os.makedirs(os.path.join(path, "device-types"))
        #             os.makedirs(os.path.join(path, "device-types", "Cisco"))
        #             with open(os.path.join(path, "device-types", "Cisco", "fake.yaml"), "w", encoding="utf8") as file:
        #                 yaml.dump(
        #                     {"manufacturer": "Cisco", "model": "Fake Model"},
        #                     file,
        #                 )
        #             with open(os.path.join(path, "device-types", "Cisco", "fake2.yml"), "w", encoding="utf8") as file:
        #                 yaml.dump(
        #                     {"manufacturer": "Cisco", "model": "Fake Model 2"},
        #                     file,
        #                 )
        #             return mock.DEFAULT

        #         mock_git_repo.side_effect = populate_repo
        #         mock_git_repo.return_value.checkout.return_value = self.COMMIT_HEXSHA

        #         enqueue_pull_git_repository_and_refresh_data(self.repo, self.user)

        with tempfile.TemporaryDirectory() as tempdir:
            with self.settings(GIT_ROOT=tempdir):

                def populate_repo(path, _url):
                    os.makedirs(path)
                    # Load device-types data for git-repository
                    os.makedirs(os.path.join(path, "device-types"))
                    os.makedirs(os.path.join(path, "device-types", "Cisco"))
                    with open(os.path.join(path, "device-types", "Cisco", "fake.yaml"), "w", encoding="utf8") as file:
                        yaml.dump(
                            {"manufacturer": "Cisco", "model": "Fake Model"},
                            file,
                        )
                    with open(os.path.join(path, "device-types", "Cisco", "fake2.yml"), "w", encoding="utf8") as file:
                        yaml.dump(
                            {"manufacturer": "Cisco", "model": "Fake Model 2"},
                            file,
                        )
                    return mock.DEFAULT

                mock_git_repo.side_effect = populate_repo
                mock_git_repo.return_value.checkout.return_value = (self.COMMIT_HEXSHA, True)

                # Run the Git operation and refresh the object from the DB
                job_model = GitRepositorySync().job_model
                job_result = run_job_for_testing(job=job_model, repository=self.repo.pk)
                job_result.refresh_from_db()
                self.assertEqual(
                    job_result.status,
                    JobResultStatusChoices.STATUS_SUCCESS,
                    (
                        job_result.result,
                        list(job_result.job_log_entries.filter(log_level="error").values_list("message", flat=True)),
                    ),
                )

                # Make sure ManufacturerImport was successfully loaded from file
                manufacturer_import = ManufacturerImport.objects.get(name="Cisco")
                self.assertIsNotNone(manufacturer_import)

                # Make sure DeviceTypeImport was successfully loaded from file
                device_type = DeviceTypeImport.objects.get(filename="fake.yaml")
                self.assertIsNotNone(device_type)
                self.assertEqual(device_type.name, "Fake Model")
                self.assertEqual(device_type.manufacturer, manufacturer_import)
                device_type2 = DeviceTypeImport.objects.get(filename="fake2.yml")
                self.assertIsNotNone(device_type2)
                self.assertEqual(device_type2.name, "Fake Model 2")

                # Delete the GitRepository (this is a noop)
                self.repo.delete()
