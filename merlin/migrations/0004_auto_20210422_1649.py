# Generated by Django 3.1.8 on 2021-04-22 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merlin', '0003_merlin_sites'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='merlin',
            name='all_completed',
        ),
        migrations.RemoveField(
            model_name='merlin',
            name='circuit_types',
        ),
        migrations.RemoveField(
            model_name='merlin',
            name='cluster_types',
        ),
        migrations.RemoveField(
            model_name='merlin',
            name='device_roles',
        ),
        migrations.RemoveField(
            model_name='merlin',
            name='device_types',
        ),
        migrations.RemoveField(
            model_name='merlin',
            name='manufacturers',
        ),
        migrations.RemoveField(
            model_name='merlin',
            name='platforms',
        ),
        migrations.RemoveField(
            model_name='merlin',
            name='providers',
        ),
        migrations.RemoveField(
            model_name='merlin',
            name='rirs',
        ),
        migrations.RemoveField(
            model_name='merlin',
            name='sites',
        ),
        migrations.AddField(
            model_name='merlin',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='merlin',
            name='ignored',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='merlin',
            name='merlin_link',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='merlin',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='merlin',
            name='nautobot_add_link',
            field=models.CharField(default='', max_length=48),
        ),
        migrations.AddField(
            model_name='merlin',
            name='nautobot_model',
            field=models.CharField(default='', max_length=48),
        ),
    ]
