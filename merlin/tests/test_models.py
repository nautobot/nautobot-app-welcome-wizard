"""Merlin Tests."""
from django.test import TestCase

from ..models.merlin import Merlin


class MerlinModelTest(TestCase):
    """Model Test Case."""
    def test_base_setup_all_false(self):
        base = Merlin()
        self.assertFalse(base.manufacturers)
        self.assertFalse(base.platforms)
        self.assertFalse(base.all_completed)
        self.assertFalse(base.device_types)
        self.assertFalse(base.device_roles)
        self.assertFalse(base.rirs)
        self.assertFalse(base.cluster_types)
        self.assertFalse(base.circuit_types)
        self.assertFalse(base.providers)
