# Generated by Django 3.1.5 on 2021-01-16 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0012_remove_conreqconfig_conreq_base_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conreqconfig',
            name='radarr_enabled',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='conreqconfig',
            name='sonarr_enabled',
            field=models.BooleanField(default=False),
        ),
    ]
