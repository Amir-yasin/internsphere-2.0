# Generated by Django 5.1.1 on 2024-12-10 08:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internSphereApp', '0002_alter_company_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('order', models.PositiveIntegerField(unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='feedback',
        ),
        migrations.RemoveField(
            model_name='evaluation',
            name='score',
        ),
        migrations.AddField(
            model_name='evaluation',
            name='assigned_supervisor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='supervisor_evaluations', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evaluation',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='department_approval_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='department_approval_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='icu_approval_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='icu_approval_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='submission_date',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='evaluation',
            name='supervisor_approval_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='supervisor_approval_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending', max_length=10),
        ),
        migrations.AddField(
            model_name='evaluation',
            name='total_score',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_evaluations', to='internSphereApp.company'),
        ),
        migrations.AlterField(
            model_name='evaluation',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_evaluations', to='internSphereApp.stud_profile'),
        ),
        migrations.CreateModel(
            name='EvaluationAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField(choices=[(5, 'Excellent'), (4, 'Good'), (3, 'Average'), (2, 'Fair'), (1, 'Poor')])),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='internSphereApp.evaluation')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='internSphereApp.evaluationquestion')),
            ],
        ),
    ]
