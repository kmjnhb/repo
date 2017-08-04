# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-04 15:46
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20170804_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='is_client',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
