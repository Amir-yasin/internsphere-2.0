# Generated by Django 5.1.1 on 2024-12-15 17:33

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internSphereApp', '0003_delete_evaluation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_1', models.PositiveIntegerField(default=0)),
                ('question_2', models.PositiveIntegerField(default=0)),
                ('question_3', models.PositiveIntegerField(default=0)),
                ('question_4', models.PositiveIntegerField(default=0)),
                ('question_5', models.PositiveIntegerField(default=0)),
                ('question_6', models.PositiveIntegerField(default=0)),
                ('question_7', models.PositiveIntegerField(default=0)),
                ('question_8', models.PositiveIntegerField(default=0)),
                ('question_9', models.PositiveIntegerField(default=0)),
                ('question_10', models.PositiveIntegerField(default=0)),
                ('question_11', models.PositiveIntegerField(default=0)),
                ('question_12', models.PositiveIntegerField(default=0)),
                ('question_13', models.PositiveIntegerField(default=0)),
                ('question_14', models.PositiveIntegerField(default=0)),
                ('question_15', models.PositiveIntegerField(default=0)),
                ('question_16', models.PositiveIntegerField(default=0)),
                ('question_17', models.PositiveIntegerField(default=0)),
                ('question_18', models.PositiveIntegerField(default=0)),
                ('question_19', models.PositiveIntegerField(default=0)),
                ('question_20', models.PositiveIntegerField(default=0)),
                ('question_21', models.PositiveIntegerField(default=0)),
                ('question_22', models.PositiveIntegerField(default=0)),
                ('question_23', models.PositiveIntegerField(default=0)),
                ('total_score', models.PositiveIntegerField(default=0)),
                ('company_approval_status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('company_approval_date', models.DateTimeField(blank=True, null=True)),
                ('internship_office_approval_status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('internship_office_approval_date', models.DateTimeField(blank=True, null=True)),
                ('department_approval_status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('department_approval_date', models.DateTimeField(blank=True, null=True)),
                ('supervisor_approval_status', models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10)),
                ('supervisor_approval_date', models.DateTimeField(blank=True, null=True)),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='internSphereApp.company')),
                ('student', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='evaluation', to='internSphereApp.stud_profile')),
            ],
        ),
    ]
