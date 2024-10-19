# Generated by Django 5.1.1 on 2024-10-18 14:04

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internSphereApp', '0003_alter_student_profile_skills'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internship_office',
            name='user',
        ),
        migrations.RenameField(
            model_name='biweeklyreport',
            old_name='report_content',
            new_name='assignment_responsibilities',
        ),
        migrations.RenameField(
            model_name='biweeklyreport',
            old_name='report_period_end',
            new_name='week_end',
        ),
        migrations.RenameField(
            model_name='biweeklyreport',
            old_name='report_period_start',
            new_name='week_start',
        ),
        migrations.RenameField(
            model_name='company',
            old_name='address',
            new_name='company_address',
        ),
        migrations.RenameField(
            model_name='evaluation',
            old_name='comments',
            new_name='feedback',
        ),
        migrations.RenameField(
            model_name='student_profile',
            old_name='full_name',
            new_name='temporary_password',
        ),
        migrations.RemoveField(
            model_name='biweeklyreport',
            name='submitted_at',
        ),
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='department',
            name='contact_email',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='evaluated_at',
        ),
        migrations.RemoveField(
            model_name='internship',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='student_profile',
            name='major',
        ),
        migrations.RemoveField(
            model_name='student_profile',
            name='university',
        ),
        migrations.RemoveField(
            model_name='supervisor',
            name='contact_email',
        ),
        migrations.RemoveField(
            model_name='supervisor',
            name='created_at',
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='administrative_hours',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='assisting_hours',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='course_relevance_suggestions',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='critical_analysis',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='date_submitted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='meetings_discussions',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='misc_hours',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='observing_hours',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='report_number',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='researching_hours',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='biweeklyreport',
            name='total_hours_completed',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='company_description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='company_phone',
            field=models.CharField(default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='department',
            name='department_head',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='internship',
            name='posted_on',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='internship',
            name='status',
            field=models.CharField(default='Open', max_length=10),
        ),
        migrations.AddField(
            model_name='student_profile',
            name='batch',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student_profile',
            name='list_of_students',
            field=models.FileField(default=1, upload_to='list_of_students/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='student_profile',
            name='profile_completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='student_profile',
            name='section',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='company_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='company',
            name='user',
            field=models.OneToOneField(limit_choices_to={'user_type': 'Company'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='user_type',
            field=models.CharField(choices=[('Student', 'Student'), ('Company', 'Company'), ('Department', 'Department'), ('Supervisor', 'Supervisor'), ('Admin', 'Admin'), ('InternshipCareerOffice', 'Internship & Career Office')], max_length=50),
        ),
        migrations.AlterField(
            model_name='department',
            name='department_name',
            field=models.CharField(choices=[('Accounting', 'Accounting'), ('Computer Science', 'Computer Science'), ('Management', 'Management'), ('Marketing', 'Marketing'), ('THM', 'THM')], max_length=50),
        ),
        migrations.AlterField(
            model_name='department',
            name='user',
            field=models.OneToOneField(limit_choices_to={'user_type': 'Department'}, on_delete=django.db.models.deletion.CASCADE, related_name='department_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='score',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='supervisor',
            name='user',
            field=models.OneToOneField(limit_choices_to={'user_type': 'Supervisor'}, on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FinalReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.FileField(upload_to='final-reports/')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internSphereApp.student_profile')),
            ],
        ),
        migrations.CreateModel(
            name='InternshipCareerOffice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ICU_director', models.CharField(max_length=100)),
                ('user', models.OneToOneField(limit_choices_to={'user_type': 'InternshipCareerOffice'}, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Admin',
        ),
        migrations.DeleteModel(
            name='Internship_Office',
        ),
    ]
