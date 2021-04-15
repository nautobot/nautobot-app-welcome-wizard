from nautobot.utilities.testing.views import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from nautobot.dcim.models import Manufacturer, DeviceType

from merlin.models.importer import DeviceTypeImport, ManufacturerImport

User = get_user_model()


class ManufacturerTestCase(TestCase):
    def test_manufacturer_bulk_import(self):
        ManufacturerImport.objects.create(name="Acme", slug="acme")
        # Ensure we can add a new manufacturer
        self.add_permissions("dcim.add_manufacturer", "dcim.view_manufacturer")

        data = {"pk": [ManufacturerImport.objects.first().pk]}
        self.client.post(reverse("plugins:merlin:manufacturer_import"), data=data, follow=True)
        manufacturer = Manufacturer.objects.get(name="Acme")
        self.assertIsNotNone(manufacturer)


class DeviceTypeTestCase(TestCase):
    def test_devicetype_bulk_import(self):
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
            "dcim.add_manufacturer", "dcim.view_manufacturer", "dcim.add_devicetype", "dcim.view_devicetype"
        )

        data = {"pk": [DeviceTypeImport.objects.first().pk]}
        self.client.post(reverse("plugins:merlin:devicetype_import"), data=data, follow=True)
        devicetype = DeviceType.objects.get(model="shelf-2he")
        self.assertIsNotNone(devicetype)
