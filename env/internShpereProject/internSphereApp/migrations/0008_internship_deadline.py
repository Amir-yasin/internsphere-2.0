# Generated by Django 5.1.1 on 2024-11-06 18:35

import internSphereApp.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internSphereApp', '0007_company_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='internship',
            name='deadline',
            field=models.DateField(default=internSphereApp.models.default_deadline, null=True),
        ),
    ]