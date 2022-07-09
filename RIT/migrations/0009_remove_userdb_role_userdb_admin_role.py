# Generated by Django 4.0.4 on 2022-06-18 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RIT', '0008_incidentdb_incident_resolution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdb',
            name='role',
        ),
        migrations.AddField(
            model_name='userdb',
            name='admin_role',
            field=models.BooleanField(default=False, verbose_name='admin_role'),
            preserve_default=False,
        ),
    ]
