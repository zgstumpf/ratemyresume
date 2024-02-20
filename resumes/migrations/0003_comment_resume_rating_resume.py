# Generated by Django 5.0.2 on 2024-02-20 14:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0002_rename_user_id_comment_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='resume',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='resumes.resume'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='resume',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='resumes.resume'),
            preserve_default=False,
        ),
    ]
