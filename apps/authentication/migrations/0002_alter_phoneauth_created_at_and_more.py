# Generated by Django 5.1.3 on 2024-12-01 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneauth',
            name='created_at',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='phoneauth',
            name='phone_number',
            field=models.CharField(max_length=12),
        ),
    ]
