# Generated by Django 3.1.3 on 2021-05-30 09:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_billingaddress'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.billingaddress'),
        ),
    ]
