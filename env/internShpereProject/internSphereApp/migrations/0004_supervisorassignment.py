# Generated by Django 5.1.1 on 2025-01-23 19:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internSphereApp', '0003_attendance'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupervisorAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_on', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='internSphereApp.stud_profile')),
                ('supervisor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assignments', to='internSphereApp.supervisor')),
            ],
        ),
    ]
