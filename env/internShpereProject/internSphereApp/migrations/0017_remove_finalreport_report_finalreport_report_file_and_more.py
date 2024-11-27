# Generated by Django 5.1.1 on 2024-11-26 10:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internSphereApp', '0016_remove_department_date_registered_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='finalreport',
            name='report',
        ),
        migrations.AddField(
            model_name='finalreport',
            name='report_file',
            field=models.FileField(default=1993, upload_to='final_reports/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='finalreport',
            name='submitted_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='finalreport',
            name='student',
            field=models.OneToOneField(limit_choices_to={'user_type': 'Student'}, on_delete=django.db.models.deletion.CASCADE, related_name='final_report', to='internSphereApp.stud_profile'),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='department',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='supervisors', to='internSphereApp.department'),
        ),
    ]
