"""Tests for Welcome Wizard Views."""

from django.contrib.auth import get_user_model
from django.test import Client, override_settings
from django.urls import reverse
from nautobot.apps.testing import TransactionTestCase
from nautobot.core.testing.utils import extract_form_failures
from nautobot.core.testing.views import TestCase
from nautobot.core.utils import permissions
from nautobot.dcim.models import DeviceType, Location, LocationType, Manufacturer
from nautobot.extras.models import Status
from nautobot.users import models as users_models
from nautobot.virtualization.models import Cluster, ClusterType

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport

User = get_user_model()


class WizardTestCaseMixin:
    """Mixin for WelcomeWizard Tests."""

    model = models.ManufacturerImport
    bulk_edit_data = {"description": "Bulk edit views"}
    form_data = {
        "name": "Test 1",
        "description": "Initial model",
    }

    update_data = {
        "name": "Test 2",
        "description": "Updated model",
    }

    def test_devicetype_list_permission_denied(self):
        """Tests the DeviceTypeImport List View with no pemissions."""
        response = self.client.get(reverse("plugins:welcome_wizard:devicetypes"))
        self.assertHttpStatus(response, 403)

    def test_devicetype_detail_view(self):
        """Tests the DeviceTypeImport Detail View"""
        self.add_permissions("welcome_wizard.view_devicetypeimport")
        manufacturer = ManufacturerImport.objects.create(name="Generic")
        device_type = DeviceTypeImport.objects.create(
            name="shelf-4he",
            filename="shelf-4he.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Generic",
                "model": "shelf-4he",
                "u_height": 4,
                "full_depth": False,
            },
        )
        response = self.client.get(
            reverse("plugins:welcome_wizard:devicetype", kwargs={"pk": device_type.id}),
        )
        self.assertHttpStatus(response, 200)


class DashboardView(TransactionTestCase):
    """Tests for dashboard view.

    Args:
        TestCase (TestCase): Generic Test Case
    """

    def setUp(self):
        self.active_status, _ = Status.objects.get_or_create(name="Active")
        super().setUp()

    def test_dashboard_view_no_entries(self):
        self.add_permissions("welcome_wizard.view_merlin")
        url = reverse("plugins:welcome_wizard:dashboard")
        resp = self.client.get(url)
        self.assertHttpStatus(resp, 200)
        self.assertContains(resp, "Dashboard")
        self.assertContains(resp, "mdi-wizard-hat", 2)
        # 9th is from nautobot formset javascript
        self.assertContains(resp, "mdi-plus-thick", 9)
        self.assertContains(resp, "mdi-checkbox-blank-outline", 8)
        self.assertContains(resp, "mdi-checkbox-marked-outline", 0)

    def test_dashboard_view_with_content(self):
        # Setup a location and manufacturer
        self.add_permissions("welcome_wizard.view_merlin")
        Manufacturer.objects.create(name="Manufacturer1")
        site, _ = LocationType.objects.get_or_create(name="Site")
        Location.objects.create(name="site01", location_type=site, status=self.active_status)
        url = reverse("plugins:welcome_wizard:dashboard")
        resp = self.client.get(url)
        self.assertHttpStatus(resp, 200)
        self.assertContains(resp, "Dashboard")
        self.assertContains(resp, "mdi-wizard-hat", 2)
        # 9th is from nautobot formset javascript
        self.assertContains(resp, "mdi-plus-thick", 9)
        self.assertContains(resp, "mdi-checkbox-blank-outline", 6)
        self.assertContains(resp, "mdi-checkbox-marked-outline", 2)

    def test_dashboard_view_permission_denied(self):
        """Test failed connection."""
        url = reverse("plugins:welcome_wizard:dashboard")
        resp = self.client.get(url)
        self.assertHttpStatus(resp, 403)


class MiddlewareTestCase(TransactionTestCase):
    """Tests the Middleware."""

    def test_middleware_missing_required(self):
        """Test middleware when dcim:devicetype is missing required fields."""
        self.add_permissions(
            "dcim.add_devicetype",
            "dcim.view_devicetype",
        )

        response = self.client.get(reverse("dcim:devicetype_add"))
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]),
            "You need to configure a <a href='/dcim/manufacturers/add/'>Manufacturer</a> before you create this item.",
        )
        self.assertHttpStatus(response, 200)

    def test_middleware_no_missing_required(self):
        """Test middleware when dcim:devicetype is not missing required fields."""
        Manufacturer.objects.create(name="Generic")
        self.add_permissions(
            "dcim.add_devicetype",
            "dcim.view_devicetype",
        )

        response = self.client.get(reverse("dcim:devicetype_add"))
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 0)
        self.assertHttpStatus(response, 200)

    def test_middleware_exceptions(self):
        """Ensure middleware exception does not break pages."""
        self.add_permissions(
            "circuits.add_circuit",
            "circuits.view_circuit",
        )

        response = self.client.get(reverse("circuits:circuit_add"))
        messages = list(response.context["messages"])
        self.assertEqual(len(messages), 2)
        self.assertHttpStatus(response, 200)


class BannerTestCase(TestCase):
    """Tests the Banner."""

    def test_banner_homeview(self):
        self.add_permissions("welcome_wizard.view_merlin")
        response = self.client.get(reverse("home"))
        self.assertContains(
            response,
            '<a href="/plugins/welcome_wizard/dashboard/">The Nautobot Welcome Wizard can help you get started with Nautobot!</a>',
        )

    def test_banner_no_permissions(self):
        response = self.client.get(reverse("home"))
        self.assertNotContains(
            response,
            '<a href="/plugins/welcome_wizard/dashboard/">The Nautobot Welcome Wizard can help you get started with Nautobot!</a>',
        )


class ClusterDevicesTestCase(TestCase):
    """Ensure Cluster Add Devices view loads (https://github.com/nautobot/nautobot-app-welcome-wizard/issues/62)."""

    def test_cluster_add_devices(self):
        self.add_permissions("virtualization.change_cluster")
        cluster_type = ClusterType.objects.create(name="Cluster Type 1")
        cluster = Cluster.objects.create(name="Cluster 1", cluster_type=cluster_type)

        self.assertHttpStatus(
            self.client.get(reverse("virtualization:cluster_add_devices", kwargs={"pk": cluster.pk})), 200
        )
