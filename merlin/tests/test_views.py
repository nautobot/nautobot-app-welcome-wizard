"""Tests for Merlin Views."""

from django.contrib.auth import get_user_model
from django.urls import reverse

from nautobot.dcim.models import Manufacturer, DeviceType
from nautobot.utilities.testing.views import TestCase

from merlin.models.importer import DeviceTypeImport, ManufacturerImport

User = get_user_model()


class ManufacturerTestCase(TestCase):
    """Tests the ManufacturerImport Views."""

    def test_manufacturer_bulk_import_permission_denied(self):
        """Tests the ManufacturerImport Bulk Import View with no pemissions."""
        ManufacturerImport.objects.create(name="Acme", slug="acme")
        self.add_permissions("merlin.view_manufacturerimport")
        data = {"pk": [ManufacturerImport.objects.first().pk]}
        response = self.client.post(reverse("plugins:merlin:manufacturer_import"), data=data, follow=True)
        self.assertHttpStatus(response, 403)
        try:
            Manufacturer.objects.get(name="Acme")
            self.fail("Manufacturer object should not exist.")
        except Manufacturer.DoesNotExist:
            pass

    def test_manufacturer_bulk_import(self):
        """Tests the ManufacturerImport Bulk Import View with correct pemissions."""
        ManufacturerImport.objects.create(name="Acme", slug="acme")
        # Ensure we can add a new manufacturer
        self.add_permissions("dcim.add_manufacturer", "dcim.view_manufacturer", "merlin.view_manufacturerimport")

        data = {"pk": [ManufacturerImport.objects.first().pk]}
        response = self.client.post(reverse("plugins:merlin:manufacturer_import"), data=data, follow=True)
        self.assertHttpStatus(response, 200)
        manufacturer = Manufacturer.objects.get(name="Acme")
        self.assertIsNotNone(manufacturer)

    def test_manufacturer_list(self):
        """Tests the ManufacturerImport List View with correct pemissions."""
        self.add_permissions("merlin.view_manufacturerimport")
        response = self.client.get(reverse("plugins:merlin:manufacturer"))
        self.assertHttpStatus(response, 200)

    def test_manufacturer_list_permission_denied(self):
        """Tests the ManufacturerImport List View with no pemissions."""
        response = self.client.get(reverse("plugins:merlin:manufacturer"))
        self.assertHttpStatus(response, 403)


class DeviceTypeTestCase(TestCase):
    """Tests the DeviceTypeImport Views."""

    def test_devicetype_bulk_import_permission_denied(self):
        """Tests the DeviceTypeImport Bulk Import View with no pemissions."""
        manufacturer = ManufacturerImport.objects.create(name="Generic", slug="generic")
        Manufacturer.objects.create(name="Generic", slug="generic")
        DeviceTypeImport.objects.create(
            name="shelf-2he",
            filename="shelf-2he.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Generic",
                "model": "shelf-2he",
                "slug": "shelf-2he",
                "u_height": 2,
                "full_depth": False,
            },
        )
        self.add_permissions("merlin.view_devicetypeimport")
        data = {"pk": [DeviceTypeImport.objects.first().pk]}
        response = self.client.post(reverse("plugins:merlin:devicetype_import"), data=data, follow=True)
        self.assertHttpStatus(response, 403)
        try:
            DeviceType.objects.get(model="shelf-2he")
            self.fail("DeviceType Object should not exist.")
        except DeviceType.DoesNotExist:
            pass

    def test_devicetype_bulk_import(self):
        """Tests the DeviceTypeImport Bulk Import View with correct pemissions."""
        manufacturer = ManufacturerImport.objects.create(name="Generic", slug="generic")
        Manufacturer.objects.create(name="Generic", slug="generic")
        DeviceTypeImport.objects.create(
            name="shelf-2he",
            filename="shelf-2he.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Generic",
                "model": "shelf-2he",
                "slug": "shelf-2he",
                "u_height": 2,
                "full_depth": False,
            },
        )
        # Ensure we can add a new devicetype
        self.add_permissions(
            "dcim.add_manufacturer",
            "dcim.view_manufacturer",
            "dcim.add_devicetype",
            "dcim.view_devicetype",
            "merlin.view_devicetypeimport",
        )

        data = {"pk": [DeviceTypeImport.objects.first().pk]}
        response = self.client.post(reverse("plugins:merlin:devicetype_import"), data=data, follow=True)
        self.assertHttpStatus(response, 200)
        devicetype = DeviceType.objects.get(model="shelf-2he")
        self.assertIsNotNone(devicetype)

    def test_devicetype_list(self):
        """Tests the DeviceTypeImport List View with correct pemissions."""
        self.add_permissions("merlin.view_devicetypeimport")
        response = self.client.get(reverse("plugins:merlin:devicetype"))
        self.assertHttpStatus(response, 200)

    def test_devicetype_list_permission_denied(self):
        """Tests the DeviceTypeImport List View with no pemissions."""
        response = self.client.get(reverse("plugins:merlin:devicetype"))
        self.assertHttpStatus(response, 403)
