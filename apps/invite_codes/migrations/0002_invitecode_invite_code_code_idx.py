# Generated by Django 5.1.3 on 2024-12-06 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invite_codes', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='invitecode',
            index=models.Index(fields=['code'], name='invite_code_code_idx'),
        ),
    ]
