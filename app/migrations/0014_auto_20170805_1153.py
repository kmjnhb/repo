# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-05 11:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20170805_1015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='manager',
            old_name='fradmin',
            new_name='fadmin',
        ),
    ]
