# Generated by Django 3.1.3 on 2021-05-21 15:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_item_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='slug',
            field=models.SlugField(),
        ),
    ]