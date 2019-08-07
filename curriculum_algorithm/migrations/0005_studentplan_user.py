# Generated by Django 2.2.1 on 2019-07-26 01:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('curriculum_algorithm', '0004_auto_20190709_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentplan',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE,
                                    to=settings.AUTH_USER_MODEL),
        ),
    ]