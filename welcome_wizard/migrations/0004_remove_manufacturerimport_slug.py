# Generated by Django 3.2.23 on 2023-11-02 19:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("welcome_wizard", "0003_auto_20210705_1912"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="manufacturerimport",
            name="slug",
        ),
    ]
