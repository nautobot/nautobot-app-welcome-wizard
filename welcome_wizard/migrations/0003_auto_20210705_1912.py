# Generated by Django 3.1.12 on 2021-07-05 19:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("welcome_wizard", "0002_merlin_nautobot_list_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="merlin",
            name="merlin_link",
            field=models.CharField(blank=True, default="", max_length=200),
        ),
    ]