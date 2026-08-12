"""Tests for Welcome Wizard Datasources."""

from unittest.mock import MagicMock, Mock, mock_open, patch

from django.conf import settings
from django.test import override_settings
from nautobot.apps.testing import TransactionTestCase
from nautobot.extras.models import JobResult

from welcome_wizard.datasources import (
    get_manufacturer_name,
    refresh_git_import_wizard,
    retrieve_device_type_images_from_filesystem,
    retrieve_device_types_from_filesystem,
)
from welcome_wizard.models.importer import DeviceTypeImageImport, DeviceTypeImport, ManufacturerImport


class TestDatasources(TransactionTestCase):
    """Test Datasources."""

    @override_settings(PLUGINS_CONFIG={"welcome_wizard": {}})
    def test_retrieve_device_types_from_filesystem_without_manufacturer_transformation(self):
        """test retrieval of Manufacturers and DeviceTypes from the filesystem without Manufacturer name transformation."""
        # provided by device_type_fixture.yaml
        device_types_data = {
            "device_type_fixture1.yaml": {
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
                "front_image": True,
                "rear_image": True,
            },
            "device_type_fixture2.yaml": {
                "manufacturer": "cIsCo",
                "model": "Catalyst 9600-33QC",
                "slug": "cisco-c9600-33qc",
                "part_number": "C9600-33QC",
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
            },
            "device_type_fixture3.yaml": {
                "manufacturer": "Cisco",
                "model": "Catalyst 9700-34QC",
                "slug": "cisco-c9700-34qc",
                "part_number": "C9700-34QC",
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
            },
        }

        manufacturers, device_types = retrieve_device_types_from_filesystem("welcome_wizard/tests/fixtures")

        self.assertEqual({"Cisco", "cIsCo"}, manufacturers)
        self.assertEqual(device_types_data, device_types)

    def test_retrieve_device_types_from_filesystem_with_manufacturer_transformation(self):
        """test retrieval of Manufacturers and DeviceTypes from the filesystem with Manufacturer name transformation."""
        # provided by device_type_fixture.yaml
        device_types_data = {
            "device_type_fixture1.yaml": {
                "manufacturer": "CISCO",
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
                "front_image": True,
                "rear_image": True,
            },
            "device_type_fixture2.yaml": {
                "manufacturer": "CiScO",
                "model": "Catalyst 9600-33QC",
                "slug": "cisco-c9600-33qc",
                "part_number": "C9600-33QC",
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
            },
            "device_type_fixture3.yaml": {
                "manufacturer": "CISCO",
                "model": "Catalyst 9700-34QC",
                "slug": "cisco-c9700-34qc",
                "part_number": "C9700-34QC",
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
            },
        }

        # Set settings.PLUGINS_CONFIG["welcome_wizard"] to force transformation
        settings.PLUGINS_CONFIG["welcome_wizard"] = {
            "manufacturer_transform_func": str.upper,
            "manufacturer_map": {
                "cIsCo": "CiScO",
            },
        }

        manufacturers, device_types = retrieve_device_types_from_filesystem("welcome_wizard/tests/fixtures")

        self.assertEqual({"CISCO", "CiScO"}, manufacturers)
        self.assertEqual(device_types_data, device_types)

    @patch("pathlib.Path")
    @patch("builtins.open", new_callable=mock_open, read_data=b"fake image data")
    @patch("django.core.files.uploadedfile.InMemoryUploadedFile")
    def test_retrieve_device_type_images_from_filesystem(self, mock_inmemoryuploadedfile, mock_file, mock_path_class):
        """Test retrieval of device type images."""
        fake_image = Mock()
        fake_image.suffix = ".png"
        mock_path_instance = Mock()
        mock_path_instance.rglob.return_value = [fake_image]
        mock_path_class.return_value = mock_path_instance

        images = retrieve_device_type_images_from_filesystem("fake/path")

        self.assertEqual(mock_file.call_count, 1)
        self.assertEqual(mock_inmemoryuploadedfile.call_count, 1)
        self.assertEqual(len(images), 1)

    def test_refresh_git_import_wizard_without_manufacturer_transformation(self):
        repository_record = MagicMock()
        repository_record.filesystem_path = "welcome_wizard/tests/fixtures"
        repository_record.provided_contents = "welcome_wizard.import_wizard"
        job_result = JobResult()
        job_result.log = MagicMock(return_value=None)

        # Unset settings.PLUGINS_CONFIG["welcome_wizard"] to avoid transformation
        settings.PLUGINS_CONFIG["welcome_wizard"] = {}

        refresh_git_import_wizard(repository_record=repository_record, job_result=job_result)

        manufacturer = ManufacturerImport.objects.get(name="Cisco")
        device_type = DeviceTypeImport.objects.get(name="Catalyst 9500-32QC")
        self.assertIsNotNone(manufacturer)
        self.assertIsNotNone(device_type)

        manufacturer = ManufacturerImport.objects.get(name="cIsCo")
        device_type = DeviceTypeImport.objects.get(name="Catalyst 9600-33QC")
        self.assertIsNotNone(manufacturer)
        self.assertIsNotNone(device_type)

        manufacturer = ManufacturerImport.objects.get(name="Cisco")
        device_type = DeviceTypeImport.objects.get(name="Catalyst 9700-34QC")
        self.assertIsNotNone(manufacturer)
        self.assertIsNotNone(device_type)

        for image_name in ("juniper-mx80.front.png", "juniper-mx80.rear.png"):
            devtype_image = DeviceTypeImageImport.objects.get(name=image_name)
            self.assertIsNotNone(devtype_image)

    def test_refresh_git_import_wizard_with_manufacturer_transformation(self):
        repository_record = MagicMock()
        repository_record.filesystem_path = "welcome_wizard/tests/fixtures"
        repository_record.provided_contents = "welcome_wizard.import_wizard"
        job_result = JobResult()
        job_result.log = MagicMock(return_value=None)

        # Set settings.PLUGINS_CONFIG["welcome_wizard"] to force transformation
        settings.PLUGINS_CONFIG["welcome_wizard"] = {
            "manufacturer_transform_func": str.upper,
            "manufacturer_map": {
                "cIsCo": "CiScO",
            },
        }

        refresh_git_import_wizard(repository_record=repository_record, job_result=job_result)

        manufacturer = ManufacturerImport.objects.get(name="CISCO")
        device_type = DeviceTypeImport.objects.get(name="Catalyst 9500-32QC")
        self.assertIsNotNone(manufacturer)
        self.assertIsNotNone(device_type)

        manufacturer = ManufacturerImport.objects.get(name="CiScO")
        device_type = DeviceTypeImport.objects.get(name="Catalyst 9600-33QC")
        self.assertIsNotNone(manufacturer)
        self.assertIsNotNone(device_type)

        manufacturer = ManufacturerImport.objects.get(name="CISCO")
        device_type = DeviceTypeImport.objects.get(name="Catalyst 9700-34QC")
        self.assertIsNotNone(manufacturer)
        self.assertIsNotNone(device_type)

        for image_name in ("juniper-mx80.front.png", "juniper-mx80.rear.png"):
            devtype_image = DeviceTypeImageImport.objects.get(name=image_name)
            self.assertIsNotNone(devtype_image)

    @override_settings(
        PLUGINS_CONFIG={
            "welcome_wizard": {
                "manufacturer_map": {
                    "juniper": "Juniper Networks",
                    "cisco": "Cisco Systems",
                },
            }
        }
    )
    def test_get_manufacturer_name_without_uppercase_transformation(self):
        """Test get_manufacturer_name() does not apply transformation when transformation is not defined."""

        # Should use the map
        self.assertEqual(get_manufacturer_name("juniper"), "Juniper Networks")
        self.assertEqual(get_manufacturer_name("cisco"), "Cisco Systems")
        # Should not transform manufacturer name if not in map
        self.assertEqual(get_manufacturer_name("arista"), "arista")

    @override_settings(
        PLUGINS_CONFIG={
            "welcome_wizard": {
                "manufacturer_map": {
                    "juniper": "Juniper Networks",
                    "cisco": "Cisco Systems",
                },
                "manufacturer_transform_func": str.upper,  # Should not apply if map is used
            }
        }
    )
    def test_get_manufacturer_name_with_transformation(self):
        """Test get_manufacturer_name() applies transformation from settings.PLUGINS_CONFIG."""
        # Should use the map, not uppercase
        self.assertEqual(get_manufacturer_name("juniper"), "Juniper Networks")
        self.assertEqual(get_manufacturer_name("cisco"), "Cisco Systems")
        # Should uppercase if not in map
        self.assertEqual(get_manufacturer_name("arista"), "ARISTA")
