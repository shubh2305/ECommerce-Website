# Generated by Django 3.1.3 on 2021-05-21 15:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='slug',
            field=models.SlugField(default=models.CharField(max_length=100)),
        ),
    ]