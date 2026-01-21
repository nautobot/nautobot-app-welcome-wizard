"""Tests for Welcome Wizard Jobs."""

from nautobot.apps.testing import TransactionTestCase, run_job_for_testing
from nautobot.dcim.models import DeviceType, Manufacturer
from nautobot.extras.models import Job, JobLogEntry

from welcome_wizard.models.importer import DeviceTypeImageImport, DeviceTypeImport, ManufacturerImport


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
                "front_image": True,
                "rear_image": True,
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

        # Create DeviceTypeImageImport entries for front image, but not for rear image to test error handling
        DeviceTypeImageImport.objects.create(
            name="juniper-mx80.front.png", image="devicetype-images/juniper-mx80.front.png"
        )

        job_result = run_job_for_testing(self.import_devicetype_job, dryrun=False, filename="MX80.yaml")

        log_entries = [log_entry.message for log_entry in JobLogEntry.objects.filter(job_result=job_result)]
        self.assertIn("Imported DeviceType MX80 successfully", log_entries)

        device_type = DeviceType.objects.get(model="MX80")
        self.assertIsNotNone(device_type)
        self.assertIsNotNone(device_type.front_image)  # Test that front image was added
        # Test that rear image was not added and an error was logged
        # self.assertIsNone(device_type.rear_image)
        self.assertIn("Rear image referenced in 'MX80.yaml' YAML configuration file is not found.", log_entries)

        interfaces = device_type.interface_templates.all()
        console_ports = device_type.console_port_templates.all()
        power_ports = device_type.power_port_templates.all()
        module_bays = device_type.module_bay_templates.all()

        self.assertEqual(interfaces.count(), 5)
        self.assertEqual(power_ports.count(), 2)
        self.assertEqual(console_ports.count(), 1)
        self.assertEqual(module_bays.count(), 6)

        # Test that the job raises an error if we try to import the same DeviceType again
        job_result = run_job_for_testing(self.import_devicetype_job, dryrun=False, filename="MX80.yaml")
        log_entries = [log_entry.message for log_entry in JobLogEntry.objects.filter(job_result=job_result)]
        self.assertIn(
            "Unable to import this device_type, a DeviceType with this model (MX80) and manufacturer (Juniper) already exist.",
            log_entries,
        )
