"""Tests for Welcome Wizard Datasources."""

from unittest.mock import MagicMock

from nautobot.apps.testing import TransactionTestCase
from nautobot.extras.models import JobResult

from welcome_wizard.datasources import refresh_git_import_wizard, retrieve_device_types_from_filesystem
from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport


class TestDatasources(TransactionTestCase):
    """Test Datasources."""

    def test_retrieve_device_types_from_filesystem(self):
        """test retrieval of Manufacturers and DeviceTypes from the filesystem."""
        manufacturers, device_types = retrieve_device_types_from_filesystem("welcome_wizard/tests/fixtures")

        # provided by device_type_fixture.yaml
        device_types_data = {
            "device_type_fixture.yaml": {
                "manufacturer": "Cisco",
                "model": "Catalyst 9500-32QC",
                "slug": "cisco-c9500-32qc",
                "part_number": "C9500-32QC",
                "u_height": 1,
                "is_full_depth": True,
                "comments": "Comments Here",
                "console-ports": [{"name": "con 0", "type": "rj-45"}, {"name": "usb", "type": "usb-mini-b"}],
                "power-ports": [{"name": "PS-0", "type": "iec-60320-c14"}, {"name": "PS-1", "type": "iec-60320-c14"}],
                "interfaces": [
                    {"name": "GigabitEthernet0/0", "type": "1000base-t", "mgmt_only": True},
                    {"name": "FortyGigabitEthernet1/0/1", "type": "40gbase-x-qsfpp"},
                    {"name": "FortyGigabitEthernet1/0/2"},
                ],
            }
        }

        self.assertEqual({"Cisco"}, manufacturers)
        self.assertEqual(device_types_data, device_types)

    def test_refresh_git_import_wizard(self):
        repository_record = MagicMock()
        repository_record.filesystem_path = "welcome_wizard/tests/fixtures"
        repository_record.provided_contents = "welcome_wizard.import_wizard"
        job_result = JobResult()
        job_result.log = MagicMock(return_value=None)

        refresh_git_import_wizard(repository_record=repository_record, job_result=job_result)

        manufacturer = ManufacturerImport.objects.get(name="Cisco")
        device_type = DeviceTypeImport.objects.get(name="Catalyst 9500-32QC")
        self.assertIsNotNone(manufacturer)
        self.assertIsNotNone(device_type)
