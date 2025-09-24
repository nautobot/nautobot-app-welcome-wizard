"""Tests for Welcome Wizard Jobs."""

from unittest.mock import patch

from django.db import IntegrityError
from nautobot.apps.testing import TransactionTestCase, run_job_for_testing
from nautobot.dcim.models import DeviceType, Manufacturer
from nautobot.extras.models import Job, JobLogEntry

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport


class TestWelcomeWizardJobs(TransactionTestCase):
    """Test the Welcome Wizard Jobs."""

    databases = ("default", "job_logs")

    def setUp(self):
        self.import_manufacturer_job = Job.objects.get(
            job_class_name="WelcomeWizardImportManufacturer",
        )
        self.import_devicetype_job = Job.objects.get(
            job_class_name="WelcomeWizardImportDeviceType",
        )
        # Super() is required here to ensure the database is properly populated
        return super().setUp()

    def test_welcome_wizard_import_manufacturer(self):
        """Successfully import a Manufacturer with a Job."""
        job_result = run_job_for_testing(
            self.import_manufacturer_job, dryrun=False, manufacturer_name="Cisco Systems Inc."
        )
        log_entries = [log_entry.message for log_entry in JobLogEntry.objects.filter(job_result=job_result)]
        manufacturer = Manufacturer.objects.get(name="Cisco Systems Inc.")
        self.assertIsNotNone(manufacturer)
        self.assertIn("Created new manufacturer", log_entries)

    def test_welcome_wizard_import_devicetype(self):
        """Successfully import a DeviceType with a Job."""
        manufacturer = ManufacturerImport.objects.create(name="Juniper")
        Manufacturer.objects.create(name="Juniper")
        DeviceTypeImport.objects.create(
            name="MX80",
            filename="MX80.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Juniper",
                "model": "MX80",
                "is_full_depth": True,
                "u_height": 2,
                "interfaces": [
                    {"name": "fxp0", "type": "1000base-t", "mgmt_only": True},
                    {"name": "xe-0/0/0", "type": "10gbase-x-xfp"},
                    {"name": "xe-0/0/1", "type": "10gbase-x-xfp"},
                    {"name": "xe-0/0/2", "type": "10gbase-x-xfp"},
                    {"name": "xe-0/0/3", "type": "10gbase-x-xfp"},
                ],
                "power-ports": [
                    {
                        "name": "PEM0",
                        "type": "iec-60320-c14",
                        "maximum_draw": 500,
                        "allocated_draw": 365,
                    },
                    {
                        "name": "PEM1",
                        "type": "iec-60320-c14",
                        "maximum_draw": 500,
                        "allocated_draw": 365,
                    },
                ],
                "power-outlets": [
                    {"name": "PEM0", "type": "iec-60320-c13", "power_port": "PEM0"},
                    {"name": "PEM1", "type": "iec-60320-c13", "power_port": "PEM1"},
                ],
                "console-ports": [{"name": "Console", "type": "rj-45"}],
                "module-bays": [
                    {"name": "psu-1a", "label": "1A", "position": "1"},
                    {"name": "psu-2a", "label": "2A", "position": "2"},
                    {"name": "psu-3a", "label": "3A", "position": "3"},
                    {"name": "psu-1b", "label": "1B", "position": "4"},
                    {"name": "psu-2b", "label": "2B", "position": "5"},
                    {"name": "psu-3b", "label": "3B", "position": "6"},
                ],
                "rear-ports": [
                    {"name": "et-0/0/0", "type": "1000base-t"},
                    {"name": "et-0/0/1", "type": "1000base-t"},
                ],
                "front-ports": [
                    {"name": "et-0/0/0", "type": "1000base-t", "rear_port": "et-0/0/0"},
                    {"name": "et-0/0/1", "type": "1000base-t", "rear_port": "et-0/0/1"},
                ],
            },
        )

        job_result = run_job_for_testing(self.import_devicetype_job, dryrun=False, filename="MX80.yaml")
        device_type = DeviceType.objects.get(model="MX80")
        self.assertIsNotNone(device_type)
        log_entries = [log_entry.message for log_entry in JobLogEntry.objects.filter(job_result=job_result)]
        self.assertIn("Imported Juniper DeviceType MX80 successfully", log_entries)

        interfaces = device_type.interface_templates.all()
        console_ports = device_type.console_port_templates.all()
        power_ports = device_type.power_port_templates.all()
        module_bays = device_type.module_bay_templates.all()
        power_outlets = device_type.power_outlet_templates.all()
        rear_ports = device_type.rear_port_templates.all()
        front_ports = device_type.front_port_templates.all()

        self.assertEqual(interfaces.count(), 5)
        self.assertEqual(power_ports.count(), 2)
        self.assertEqual(console_ports.count(), 1)
        self.assertEqual(module_bays.count(), 6)
        self.assertEqual(power_outlets.count(), 2)
        self.assertEqual(rear_ports.count(), 2)
        self.assertEqual(front_ports.count(), 2)

        # Test that the job raises an error if we try to import the same DeviceType again
        job_result = run_job_for_testing(self.import_devicetype_job, dryrun=False, filename="MX80.yaml")
        log_entries = [log_entry.message for log_entry in JobLogEntry.objects.filter(job_result=job_result)]
        self.assertIn(
            "Unable to import this device_type, a DeviceType with this model (MX80) and manufacturer (Juniper) already exist.",
            log_entries,
        )

    def test_welcome_wizard_import_devicetype_handles_component_integrity_error(self):
        """Test that the job handles IntegrityError when creating components."""
        manufacturer = ManufacturerImport.objects.create(name="Juniper")
        Manufacturer.objects.create(name="Juniper")
        DeviceTypeImport.objects.create(
            name="MX80",
            filename="MX80.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Juniper",
                "model": "MX80",
                "is_full_depth": True,
                "u_height": 2,
                "interfaces": [
                    {"name": "fxp0", "type": "1000base-t", "mgmt_only": True},
                    {"name": "xe-0/0/0", "type": "10gbase-x-xfp"},
                    {"name": "xe-0/0/1", "type": "10gbase-x-xfp"},
                    {"name": "xe-0/0/2", "type": "10gbase-x-xfp"},
                    {"name": "xe-0/0/3", "type": "10gbase-x-xfp"},
                ],
                "power-ports": [
                    {
                        "name": "PEM0",
                        "type": "iec-60320-c14",
                        "maximum_draw": 500,
                        "allocated_draw": 365,
                    },
                    {
                        "name": "PEM1",
                        "type": "iec-60320-c14",
                        "maximum_draw": 500,
                        "allocated_draw": 365,
                    },
                ],
                "console-ports": [{"name": "Console", "type": "rj-45"}],
                "module-bays": [
                    {"name": "psu-1a", "label": "1A", "position": "1"},
                    {"name": "psu-2a", "label": "2A", "position": "2"},
                    {"name": "psu-3a", "label": "3A", "position": "3"},
                    {"name": "psu-1b", "label": "1B", "position": "4"},
                    {"name": "psu-2b", "label": "2B", "position": "5"},
                    {"name": "psu-3b", "label": "3B", "position": "6"},
                ],
            },
        )

        # Test that the job handles IntegrityError when creating components
        errmsg = "Simulated IntegrityError for testing"
        with patch(
            "nautobot.dcim.models.InterfaceTemplate.objects.bulk_create",
            side_effect=IntegrityError(errmsg),
        ):
            job_result = run_job_for_testing(self.import_devicetype_job, dryrun=False, filename="MX80.yaml")
            log_entries = [log_entry.message for log_entry in JobLogEntry.objects.filter(job_result=job_result)]
            self.assertIn(f"Failed to create InterfaceTemplate component(s): {errmsg}", log_entries)

    def test_welcome_wizard_import_devicetype_handles_powerporttemplate_doesnotexist(self):
        """Validates that import_components() handles case when referenced power_port does not exist."""
        manufacturer = ManufacturerImport.objects.create(name="Juniper")
        Manufacturer.objects.create(name="Juniper")
        DeviceTypeImport.objects.create(
            name="MX80",
            filename="MX80.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Juniper",
                "model": "MX80",
                "is_full_depth": True,
                "u_height": 2,
                "power-ports": [
                    {
                        "name": "PEM0",
                        "type": "iec-60320-c14",
                        "maximum_draw": 500,
                        "allocated_draw": 365,
                    },
                    {
                        "name": "PEM1",
                        "type": "iec-60320-c14",
                        "maximum_draw": 500,
                        "allocated_draw": 365,
                    },
                ],
                "power-outlets": [
                    {"name": "PEM0", "type": "iec-60320-c13", "power_port": "PEM0"},
                    {"name": "PEM2", "type": "iec-60320-c13", "power_port": "PEM2"},
                ],
            },
        )

        job_result = run_job_for_testing(self.import_devicetype_job, dryrun=False, filename="MX80.yaml")
        log_entries = [log_entry.message for log_entry in JobLogEntry.objects.filter(job_result=job_result)]
        self.assertIn("PowerPortTemplate with name 'PEM2' does not exist for DeviceType 'MX80'.", log_entries)

    def test_welcome_wizard_import_devicetype_handles_rearporttemplate_doesnotexist(self):
        """Validates that import_components() handles case when referenced rear_port does not exist."""
        manufacturer = ManufacturerImport.objects.create(name="Juniper")
        Manufacturer.objects.create(name="Juniper")
        DeviceTypeImport.objects.create(
            name="MX80",
            filename="MX80.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Juniper",
                "model": "MX80",
                "is_full_depth": True,
                "u_height": 2,
                "rear-ports": [
                    {"name": "et-0/0/0", "type": "1000base-t"},
                    {"name": "et-0/0/1", "type": "1000base-t"},
                ],
                "front-ports": [
                    {"name": "et-0/0/0", "type": "1000base-t", "rear_port": "et-0/0/0"},
                    {"name": "et-0/0/2", "type": "1000base-t", "rear_port": "et-0/0/2"},
                ],
            },
        )

        job_result = run_job_for_testing(self.import_devicetype_job, dryrun=False, filename="MX80.yaml")
        log_entries = [log_entry.message for log_entry in JobLogEntry.objects.filter(job_result=job_result)]
        self.assertIn("RearPortTemplate with name 'et-0/0/2' does not exist for DeviceType 'MX80'.", log_entries)
