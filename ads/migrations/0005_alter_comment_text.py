# Generated by Django 4.2.7 on 2025-02-26 12:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0004_alter_comment_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='text',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(3, 'Comment cant be less than 3 chars!')]),
        ),
    ]
