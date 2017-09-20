# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-12 09:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('administration', '0005_auto_20170912_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='issue_date_time',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
        migrations.AlterField(
            model_name='issue',
            name='return_date_time',
            field=models.DateTimeField(default=django.utils.timezone.now, null=True),
        ),
    ]