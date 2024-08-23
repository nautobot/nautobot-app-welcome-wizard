# Generated by Django 3.1.12 on 2021-06-29 04:26

import django.core.serializers.json
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ManufacturerImport",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.CharField(max_length=100, unique=True)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
        migrations.CreateModel(
            name="Merlin",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("name", models.CharField(default="", max_length=100)),
                ("completed", models.BooleanField(default=False)),
                ("ignored", models.BooleanField(default=False)),
                ("nautobot_model", models.CharField(default="", max_length=255)),
                ("nautobot_add_link", models.CharField(default="", max_length=255)),
                ("merlin_link", models.CharField(default="", max_length=200)),
            ],
            options={
                "verbose_name_plural": "merlin",
            },
        ),
        migrations.CreateModel(
            name="DeviceTypeImport",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("filename", models.CharField(max_length=100, unique=True)),
                ("name", models.CharField(max_length=100)),
                (
                    "device_type_data",
                    models.JSONField(blank=True, encoder=django.core.serializers.json.DjangoJSONEncoder, null=True),
                ),
                (
                    "manufacturer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="device_types",
                        to="welcome_wizard.manufacturerimport",
                    ),
                ),
            ],
            options={
                "ordering": ("name",),
            },
        ),
    ]
