# Generated by Django 5.0.2 on 2024-05-24 07:40

import resumes.formatChecker
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0017_alter_resume_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resume',
            name='file',
            field=resumes.formatChecker.ContentTypeRestrictedFileField(upload_to='resumes/'),
        ),
    ]
