# Generated by Django 5.0.3 on 2024-03-28 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kino', '0002_rename_role_role_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personsroles',
            old_name='fole',
            new_name='role',
        ),
    ]
