# Generated by Django 5.0.3 on 2024-04-01 07:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kino', '0008_alter_review_createtime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='review',
            old_name='createTime',
            new_name='create_time',
        ),
    ]
