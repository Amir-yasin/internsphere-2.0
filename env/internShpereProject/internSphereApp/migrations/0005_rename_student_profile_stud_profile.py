# Generated by Django 5.1.1 on 2024-11-02 05:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internSphereApp', '0004_remove_internship_office_user_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='student_Profile',
            new_name='stud_profile',
        ),
    ]
