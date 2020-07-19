# Generated by Django 2.2.1 on 2019-11-18 20:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('curriculum_algorithm', '0005_studentplan_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlanWarning',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True,
                                        serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=64)),
                ('target',
                 models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                   to='curriculum_algorithm.StudentPlan')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]