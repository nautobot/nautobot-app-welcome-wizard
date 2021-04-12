from django.test import TestCase

from ..models import Merlin


class MerlinModelTest(TestCase):
    def test_base_setup_all_false(self):
        base = Merlin()
        self.assertFalse(base.manufacturers)
        self.assertFalse(base.platforms)
        self.assertFalse(base.all_completed)
        self.assertFalse(base.device_types)
        self.assertFalse(base.device_roles)