# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-26 10:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marker', '0007_remove_annotation_pom_file'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Rectangle',
        ),
    ]
