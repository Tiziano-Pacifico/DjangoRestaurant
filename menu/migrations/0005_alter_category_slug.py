# Generated by Django 5.1.4 on 2025-04-05 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0004_alter_category_category_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=100),
        ),
    ]
