# Generated by Django 5.1.1 on 2024-11-20 15:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internSphereApp', '0014_remove_biweeklyreport_applicaion_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='biweeklyreport',
            name='application_status',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='internSphereApp.application'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='company_approval_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='company_approval_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='internship_office_approval_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='internship_office_approval_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='biweeklyreport',
            name='administrative_hours',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='biweeklyreport',
            name='assisting_hours',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='biweeklyreport',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='internSphereApp.company'),
        ),
        migrations.AlterField(
            model_name='biweeklyreport',
            name='misc_hours',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='biweeklyreport',
            name='observing_hours',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='biweeklyreport',
            name='report_number',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='biweeklyreport',
            name='researching_hours',
            field=models.PositiveIntegerField(),
        ),
        migrations.AlterField(
            model_name='biweeklyreport',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='internSphereApp.stud_profile'),
        ),
        migrations.AlterField(
            model_name='biweeklyreport',
            name='total_hours_completed',
            field=models.PositiveIntegerField(),
        ),
    ]