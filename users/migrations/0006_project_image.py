# Generated by Django 4.2.11 on 2024-05-01 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_workexperience_project_education_certification'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='project_images/'),
        ),
    ]
