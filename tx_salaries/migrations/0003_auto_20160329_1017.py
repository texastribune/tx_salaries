# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-29 15:17
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations
import tx_people.fields
import tx_people.utils


class Migration(migrations.Migration):

    dependencies = [
        ('tx_salaries', '0002_auto_20160327_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizationstats',
            name='female',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='organizationstats',
            name='male',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='organizationstats',
            name='races',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='organizationstats',
            name='time_employed',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='positionstats',
            name='female',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='positionstats',
            name='male',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='positionstats',
            name='races',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
        migrations.AlterField(
            model_name='positionstats',
            name='time_employed',
            field=django.contrib.postgres.fields.jsonb.JSONField(null=True),
        ),
    ]
