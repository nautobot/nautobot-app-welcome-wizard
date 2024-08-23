"""Unit tests for Welcome Wizard."""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from nautobot.users.models import Token
from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport

User = get_user_model()


class PlaceholderAPITest(TestCase):
    """Test the Welcome Wizard API."""

    def setUp(self):
        """Create a superuser and token for API calls."""
        self.user = User.objects.create(username="testuser", is_superuser=True)
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_device_type_import_api(self):
        """Verify that device type import can be listed."""
        url = reverse("plugins-api:welcome_wizard-api:devicetypeimport-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_manufacturer_import_api(self):
        """Verify that a manufacturer import can be listed."""
        url = reverse("plugins-api:welcome_wizard-api:manufacturerimport-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 0)

    def test_devicetype_with_data(self):
        """Verify that device type import shows devicetype."""
        manufacturer = ManufacturerImport(name="Acme", slug="acme")
        manufacturer.save()
        devicetype = DeviceTypeImport(
            name="acme10", manufacturer=manufacturer, filename="acme10.yaml", device_type_data={"test": "foo"}
        )
        devicetype.save()
        url = reverse("plugins-api:welcome_wizard-api:devicetypeimport-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        url = reverse("plugins-api:welcome_wizard-api:devicetypeimport-detail", kwargs={"pk": devicetype.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "acme10")
        self.assertEqual(response.data["filename"], "acme10.yaml")

    def test_manufacturer_with_data(self):
        """Verify that manufacturer import shows manufacturer."""
        manufacturer = ManufacturerImport(name="Acme", slug="acme")
        manufacturer.save()
        url = reverse("plugins-api:welcome_wizard-api:manufacturerimport-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

        url = reverse("plugins-api:welcome_wizard-api:manufacturerimport-detail", kwargs={"pk": manufacturer.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Acme")
        self.assertEqual(response.data["slug"], "acme")
