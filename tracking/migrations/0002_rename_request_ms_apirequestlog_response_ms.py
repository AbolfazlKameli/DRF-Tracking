# Generated by Django 5.0.7 on 2024-07-24 20:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracking', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='apirequestlog',
            old_name='request_ms',
            new_name='response_ms',
        ),
    ]
