# Generated by Django 5.1.1 on 2024-12-22 16:35

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internSphereApp', '0005_remove_evaluationanswer_evaluation_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='EvaluationQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('total_score', models.IntegerField(default=0)),
                ('submitted', models.BooleanField(default=False)),
                ('company_approval_status', models.CharField(default='Pending', max_length=20)),
                ('company_approval_date', models.DateTimeField(blank=True, null=True)),
                ('internship_office_approval_status', models.CharField(default='Pending', max_length=20)),
                ('internship_office_approval_date', models.DateTimeField(blank=True, null=True)),
                ('department_approval_status', models.CharField(default='Pending', max_length=20)),
                ('department_approval_date', models.DateTimeField(blank=True, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='internSphereApp.company')),
                ('internship', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='internSphereApp.internship')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='evaluations', to='internSphereApp.stud_profile')),
            ],
        ),
        migrations.CreateModel(
            name='EvaluationAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.IntegerField()),
                ('evaluation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='internSphereApp.evaluation')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='internSphereApp.evaluationquestion')),
            ],
        ),
    ]