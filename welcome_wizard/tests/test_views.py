"""Tests for Welcome Wizard Views."""

from django.contrib.auth import get_user_model
from django.test import Client, override_settings
from django.utils.text import slugify
from django.urls import reverse

from nautobot.extras.models import Tag
from nautobot.users.models import ObjectPermission
from nautobot.utilities.permissions import resolve_permission_ct
from nautobot.utilities.testing.utils import extract_form_failures

from nautobot.dcim.models import Manufacturer, DeviceType
from nautobot.dcim.models.sites import Site
from nautobot.utilities.testing import TransactionTestCase
from nautobot.utilities.testing.views import TestCase
from nautobot.virtualization.models import Cluster, ClusterType

from welcome_wizard.models.importer import DeviceTypeImport, ManufacturerImport


User = get_user_model()


class WizardTestCaseMixin:
    """Mixin for WelcomeWizard Tests. This is temporary until tests move to running against Nautobot 1.4"""

    user_permissions = ()

    def setUpWizard(self, client=True):  # pylint: disable=invalid-name
        """Setup shared testuser, statuses and client."""

        # Create the test user and assign permissions
        self.user = User.objects.create_user(username="wizard_testuser")
        self.add_permissions(*self.user_permissions)

        if client:
            # Initialize the test client
            self.client = Client()

            # Force login explicitly with the first-available backend
            self.client.force_login(self.user)

    #
    # Permissions management
    #

    def add_permissions(self, *names):
        """
        Assign a set of permissions to the test user. Accepts permission names in the form <app>.<action>_<model>.
        """
        for name in names:
            ctype, action = resolve_permission_ct(name)
            obj_perm = ObjectPermission(name=name, actions=[action])
            obj_perm.save()
            obj_perm.users.add(self.user)
            obj_perm.object_types.add(ctype)

    #
    # Custom assertions
    #

    def assertHttpStatus(self, response, expected_status, msg=None):  # pylint: disable=invalid-name
        """
        TestCase method. Provide more detail in the event of an unexpected HTTP response.
        """
        err_message = None
        # Construct an error message only if we know the test is going to fail
        if response.status_code != expected_status:
            if hasattr(response, "data"):
                # REST API response; pass the response data through directly
                err = response.data
            else:
                # Attempt to extract form validation errors from the response HTML
                form_errors = extract_form_failures(response.content.decode(response.charset))
                err = form_errors or response.content.decode(response.charset) or "No data"
            err_message = f"Expected HTTP status {expected_status}; received {response.status_code}: {err}"
            if msg:
                err_message = f"{msg}\n{err_message}"
        self.assertEqual(response.status_code, expected_status, err_message)

    def assertInstanceEqual(self, instance, data, exclude=None, api=False):  # pylint: disable=invalid-name
        """
        Compare a model instance to a dictionary, checking that its attribute values match those specified
        in the dictionary.

        :param instance: Python object instance
        :param data: Dictionary of test data used to define the instance
        :param exclude: List of fields to exclude from comparison (e.g. passwords, which get hashed)
        :param api: Set to True is the data is a JSON representation of the instance
        """
        if exclude is None:
            exclude = []

        fields = [k for k in data.keys() if k not in exclude]
        model_dict = self.model_to_dict(instance, fields=fields, api=api)

        new_model_dict = {}
        for key, value in model_dict.items():
            if isinstance(value, list):
                # Sort lists of values. This includes items like tags, or other M2M fields
                new_model_dict[key] = sorted(value)
            else:
                new_model_dict[key] = value

        # Omit any dictionary keys which are not instance attributes or have been excluded
        relevant_data = {}
        for key, value in data.items():
            if hasattr(instance, key) and key not in exclude:
                if isinstance(value, list):
                    # Sort lists of values. This includes items like tags, or other M2M fields
                    relevant_data[key] = sorted(value)
                else:
                    relevant_data[key] = value

        self.assertEqual(new_model_dict, relevant_data)

    #
    # Convenience methods
    #

    @classmethod
    def create_tags(cls, *names):
        """
        Create and return a Tag instance for each name given.
        """

        return [Tag.objects.create(name=name, slug=slugify(name)) for name in names]


class ManufacturerTestCase(TransactionTestCase, WizardTestCaseMixin):
    """Tests the ManufacturerImport Views."""

    databases = ("default", "job_logs")

    def setUp(self):
        super().setUpWizard()

    def test_manufacturer_bulk_import_permission_denied(self):
        """Tests the ManufacturerImport Bulk Import View with no permissions."""
        ManufacturerImport.objects.create(name="Alcatel", slug="alcatel")
        self.add_permissions("welcome_wizard.view_manufacturerimport")
        data = {"pk": [ManufacturerImport.objects.first().pk]}
        response = self.client.post(reverse("plugins:welcome_wizard:manufacturer_import"), data=data, follow=True)
        self.assertHttpStatus(response, 403)
        try:
            name = Manufacturer.objects.get(name="Alcatel")
            self.fail(f"{name} Manufacturer object should not exist.")
        except Manufacturer.DoesNotExist:
            pass

    def test_manufacturer_bulk_import(self):
        """Tests the ManufacturerImport Bulk Import View with correct permissions."""
        ManufacturerImport.objects.create(name="Onyx", slug="onyx")
        # Ensure we can add a new manufacturer
        self.add_permissions(
            "dcim.add_manufacturer", "dcim.view_manufacturer", "welcome_wizard.view_manufacturerimport"
        )

        data = {"pk": [ManufacturerImport.objects.first().pk]}
        response = self.client.post(reverse("plugins:welcome_wizard:manufacturer_import"), data=data, follow=True)
        self.assertHttpStatus(response, 200)
        manufacturer = Manufacturer.objects.get(name="Onyx")
        self.assertIsNotNone(manufacturer)

    def test_manufacturer_bulk_import_get(self):
        ManufacturerImport.objects.create(name="Acme", slug="acme")
        self.add_permissions(
            "dcim.add_manufacturer", "dcim.view_manufacturer", "welcome_wizard.view_manufacturerimport"
        )

        lookup_key = ManufacturerImport.objects.first().pk
        response = self.client.get(f'{reverse("plugins:welcome_wizard:manufacturer_import")}?pk={lookup_key}')
        self.assertHttpStatus(response, 200)

    def test_manufacturer_bulk_import_get_empty(self):
        self.add_permissions(
            "dcim.add_manufacturer", "dcim.view_manufacturer", "welcome_wizard.view_manufacturerimport"
        )
        response = self.client.get(reverse("plugins:welcome_wizard:manufacturer_import"), follow=True)

        self.assertRedirects(response, reverse("plugins:welcome_wizard:manufacturer"), status_code=302)

    def test_manufacturer_list(self):
        """Tests the ManufacturerImport List View with correct permissions."""
        self.add_permissions("welcome_wizard.view_manufacturerimport")
        response = self.client.get(reverse("plugins:welcome_wizard:manufacturer"))
        self.assertHttpStatus(response, 200)

    def test_manufacturer_list_permission_denied(self):
        """Tests the ManufacturerImport List View with no permissions."""
        response = self.client.get(reverse("plugins:welcome_wizard:manufacturer"))
        self.assertHttpStatus(response, 403)


class DeviceTypeTestCase(TransactionTestCase, WizardTestCaseMixin):
    """Tests the DeviceTypeImport Views."""

    databases = ("default", "job_logs")

    def setUp(self):
        super().setUpWizard()

    def test_devicetype_bulk_import_permission_denied(self):
        """Tests the DeviceTypeImport Bulk Import View with no pemissions."""
        manufacturer = ManufacturerImport.objects.create(name="Generic", slug="generic")
        Manufacturer.objects.create(name="Generic", slug="generic")
        DeviceTypeImport.objects.create(
            name="shelf-4he",
            filename="shelf-4he.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Generic",
                "model": "shelf-4he",
                "slug": "shelf-4he",
                "u_height": 4,
                "full_depth": False,
            },
        )
        self.add_permissions("welcome_wizard.view_devicetypeimport")
        data = {"pk": [DeviceTypeImport.objects.first().pk]}
        response = self.client.post(reverse("plugins:welcome_wizard:devicetype_import"), data=data, follow=True)
        self.assertHttpStatus(response, 403)
        try:
            DeviceType.objects.get(model="shelf-4he")
            self.fail("DeviceType Object should not exist.")
        except DeviceType.DoesNotExist:
            pass

    def test_devicetype_bulk_import(self):
        """Tests the DeviceTypeImport Bulk Import View with correct pemissions."""
        manufacturer = ManufacturerImport.objects.create(name="Generic", slug="generic")
        Manufacturer.objects.create(name="Generic", slug="generic")
        DeviceTypeImport.objects.create(
            name="shelf-1he",
            filename="shelf-1he.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Generic",
                "model": "shelf-1he",
                "slug": "shelf-1he",
                "u_height": 1,
                "full_depth": False,
            },
        )
        # Ensure we can add a new devicetype
        self.add_permissions(
            "dcim.add_manufacturer",
            "dcim.view_manufacturer",
            "dcim.add_devicetype",
            "dcim.view_devicetype",
            "welcome_wizard.view_devicetypeimport",
        )

        data = {"pk": [DeviceTypeImport.objects.first().pk]}
        response = self.client.post(reverse("plugins:welcome_wizard:devicetype_import"), data=data, follow=True)
        self.assertHttpStatus(response, 200)
        devicetype = DeviceType.objects.get(model="shelf-1he")
        self.assertIsNotNone(devicetype)

        # Test a duplicate import
        response = self.client.post(reverse("plugins:welcome_wizard:devicetype_import"), data=data, follow=True)
        self.assertHttpStatus(response, 200)

    def test_devicetype_list(self):
        """Tests the DeviceTypeImport List View with correct pemissions."""
        self.add_permissions("welcome_wizard.view_devicetypeimport")
        response = self.client.get(reverse("plugins:welcome_wizard:devicetype"))
        self.assertHttpStatus(response, 200)

    @override_settings(
        PLUGINS_CONFIG={
            "welcome_wizard": {
                "enable_devicetype-library": False,
            }
        },
    )
    def test_devicetype_list_override(self):
        """Tests the DeviceTypeImport List View with enable_devicetype-library False."""
        self.add_permissions("welcome_wizard.view_devicetypeimport")
        response = self.client.get(reverse("plugins:welcome_wizard:devicetype"))
        self.assertHttpStatus(response, 200)

    def test_devicetype_list_permission_denied(self):
        """Tests the DeviceTypeImport List View with no pemissions."""
        response = self.client.get(reverse("plugins:welcome_wizard:devicetype"))
        self.assertHttpStatus(response, 403)

    def test_devicetype_job_with_components(self):
        """Tests the DeviceTypeImport Bulk Import View with more data."""
        manufacturer = ManufacturerImport.objects.create(name="Juniper", slug="juniper")
        Manufacturer.objects.create(name="Juniper", slug="juniper")
        DeviceTypeImport.objects.create(
            name="MX80",
            filename="MX80.yaml",
            manufacturer=manufacturer,
            device_type_data={
                "manufacturer": "Juniper",
                "model": "MX80",
                "slug": "mx80",
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
            },
        )
        # Ensure we can add a new devicetype
        self.add_permissions(
            "dcim.add_manufacturer",
            "dcim.view_manufacturer",
            "dcim.add_devicetype",
            "dcim.view_devicetype",
            "welcome_wizard.view_devicetypeimport",
        )

        data = {"pk": [DeviceTypeImport.objects.first().pk]}
        response = self.client.post(reverse("plugins:welcome_wizard:devicetype_import"), data=data, follow=True)
        self.assertHttpStatus(response, 200)

        devicetype = DeviceType.objects.get(model="MX80")
        self.assertIsNotNone(devicetype)


class DashboardView(TestCase):
    """Tests for dashboard view.

    Args:
        TestCase (TestCase): Generic Test Case
    """

    def test_dashboard_view_no_entries(self):
        self.add_permissions("welcome_wizard.view_merlin")
        url = reverse("plugins:welcome_wizard:dashboard")
        resp = self.client.get(url)
        self.assertHttpStatus(resp, 200)
        self.assertContains(resp, "Dashboard")
        self.assertContains(resp, "mdi-wizard-hat", 2)
        self.assertContains(resp, "mdi-plus-thick", 8)
        self.assertContains(resp, "mdi-checkbox-blank-outline", 8)
        self.assertContains(resp, "mdi-checkbox-marked-outline", 0)

    def test_dashboard_view_with_content(self):
        # Setup a site and manufacturer
        self.add_permissions("welcome_wizard.view_merlin")
        Manufacturer.objects.create(name="Manufacturer1", slug="manufacturer1")
        Site.objects.create(name="site01", slug="site01")
        url = reverse("plugins:welcome_wizard:dashboard")
        resp = self.client.get(url)
        self.assertHttpStatus(resp, 200)
        self.assertContains(resp, "Dashboard")
        self.assertContains(resp, "mdi-wizard-hat", 2)
        self.assertContains(resp, "mdi-plus-thick", 8)
        self.assertContains(resp, "mdi-checkbox-blank-outline", 6)
        self.assertContains(resp, "mdi-checkbox-marked-outline", 2)

    def test_dashboard_view_permission_denied(self):
        """Test failed connection."""
        url = reverse("plugins:welcome_wizard:dashboard")
        resp = self.client.get(url)
        self.assertHttpStatus(resp, 403)


class MiddlewareTestCase(TestCase):
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
        Manufacturer.objects.create(name="Generic", slug="generic")
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
    """Ensure Cluster Add Devices view loads (https://github.com/nautobot/nautobot-plugin-welcome-wizard/issues/62)."""

    def test_cluster_add_devices(self):
        self.add_permissions("virtualization.change_cluster")
        cluster_type = ClusterType.objects.create(name="Cluster Type 1", slug="cluster-type-1")
        cluster = Cluster.objects.create(name="Cluster 1", type=cluster_type)

        self.assertHttpStatus(
            self.client.get(reverse("virtualization:cluster_add_devices", kwargs={"pk": cluster.pk})), 200
        )
