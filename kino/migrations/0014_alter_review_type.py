# Generated by Django 4.2 on 2024-04-21 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kino', '0013_alter_review_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='type',
            field=models.CharField(blank=True, choices=[('neutral', 'Нейтральный'), ('like', 'Положительный'), ('dislike', 'Отрицательный')], default='neutral', max_length=30, null=True),
        ),
    ]
