# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-16 14:16
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('georegion', '0004_georegion_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='georegion',
            name='gov_seat',
            field=django.contrib.gis.db.models.fields.PointField(blank=True, geography=True, null=True, srid=4326, verbose_name='gov seat'),
        ),
    ]
