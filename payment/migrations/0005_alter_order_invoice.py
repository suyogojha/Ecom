# Generated by Django 5.1.1 on 2024-11-23 00:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0004_order_invoice_order_paid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='invoice',
            field=models.DateTimeField(blank=True, max_length=100, null=True),
        ),
    ]