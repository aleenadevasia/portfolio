# Generated by Django 4.2.11 on 2024-04-30 01:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='contact_number',
            new_name='contact',
        ),
    ]
