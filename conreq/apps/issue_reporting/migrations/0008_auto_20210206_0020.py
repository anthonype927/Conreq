# Generated by Django 3.1.5 on 2021-02-06 08:20

from django.db import migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('issue_reporting', '0007_auto_20210204_0207'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportedissue',
            name='episode_ids',
            field=jsonfield.fields.JSONField(default='[]'),
        ),
        migrations.AlterField(
            model_name='reportedissue',
            name='episodes',
            field=jsonfield.fields.JSONField(default='[]'),
        ),
        migrations.AlterField(
            model_name='reportedissue',
            name='seasons',
            field=jsonfield.fields.JSONField(default='[]'),
        ),
    ]
