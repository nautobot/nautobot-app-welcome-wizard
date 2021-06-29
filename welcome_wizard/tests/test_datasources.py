"""Tests for Welcome Wizard Datasources."""
import os
import tempfile
from unittest import mock
import uuid

import yaml

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test import RequestFactory, TestCase

from nautobot.extras.choices import JobResultStatusChoices
from nautobot.extras.datasources.git import pull_git_repository_and_refresh_data
from nautobot.extras.datasources.registry import get_datasource_contents
from nautobot.extras.models import (
    GitRepository,
    JobResult,
)
from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport

# Use the proper swappable User model
User = get_user_model()


@mock.patch("nautobot.extras.datasources.git.GitRepo")
class GitTest(TestCase):
    """Git Tests."""

    COMMIT_HEXSHA = "88dd9cd78df89e887ee90a1d209a3e9a04e8c841"

    def setUp(self):
        """Setup tests."""
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
        self.repo.save(trigger_resync=False)

        self.job_result = JobResult(
            name=self.repo.name,
            obj_type=ContentType.objects.get_for_model(GitRepository),
            job_id=uuid.uuid4(),
        )

    def test_pull_git_repository_and_refresh_data_with_no_data(self, mock_git_repo):
        """The test_pull_git_repository_and_refresh_data job should succeed if the given repo is empty."""
        with tempfile.TemporaryDirectory() as tempdir:
            with self.settings(GIT_ROOT=tempdir):

                def create_empty_repo(path, _url):
                    os.makedirs(path)
                    return mock.DEFAULT

                mock_git_repo.side_effect = create_empty_repo
                mock_git_repo.return_value.checkout.return_value = self.COMMIT_HEXSHA

                pull_git_repository_and_refresh_data(self.repo.pk, self.dummy_request, self.job_result)

                self.assertEqual(
                    self.job_result.status,
                    JobResultStatusChoices.STATUS_COMPLETED,
                    self.job_result.data,
                )
                self.repo.refresh_from_db()
                self.assertEqual(self.repo.current_head, self.COMMIT_HEXSHA, self.job_result.data)
                # TODO: inspect the logs in job_result.data?

    def test_pull_git_repository_and_refresh_data_with_valid_data(self, mock_git_repo):
        """The test_pull_git_repository_and_refresh_data job should succeed if valid data is present in the repo."""
        with tempfile.TemporaryDirectory() as tempdir:
            with self.settings(GIT_ROOT=tempdir):

                def populate_repo(path, _url):
                    os.makedirs(path)
                    # Load device-types data for git-repository
                    os.makedirs(os.path.join(path, "device-types"))
                    os.makedirs(os.path.join(path, "device-types", "Cisco"))
                    with open(os.path.join(path, "device-types", "Cisco", "fake.yaml"), "w") as file:
                        yaml.dump(
                            {"manufacturer": "Cisco", "model": "Fake Model"},
                            file,
                        )
                    return mock.DEFAULT

                mock_git_repo.side_effect = populate_repo
                mock_git_repo.return_value.checkout.return_value = self.COMMIT_HEXSHA

                pull_git_repository_and_refresh_data(self.repo.pk, self.dummy_request, self.job_result)

                self.assertEqual(
                    self.job_result.status,
                    JobResultStatusChoices.STATUS_COMPLETED,
                    self.job_result.data,
                )

                # Make sure ManufacturerImport was successfully loaded from file
                manufacturer_import = ManufacturerImport.objects.get(name="Cisco")
                self.assertIsNotNone(manufacturer_import)

                # Make sure DeviceTypeImport was successfully loaded from file
                device_type = DeviceTypeImport.objects.get(filename="fake.yaml")
                self.assertIsNotNone(device_type)
                self.assertEqual(device_type.name, "Fake Model")
                self.assertEqual(device_type.manufacturer, manufacturer_import)

                # Delete the GitRepository (this is a noop)
                self.repo.delete()
