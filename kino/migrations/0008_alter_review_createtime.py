# Generated by Django 5.0.3 on 2024-04-01 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kino', '0007_alter_review_createtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='createTime',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
