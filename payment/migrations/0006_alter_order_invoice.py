# Generated by Django 5.1.1 on 2024-11-23 00:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0005_alter_order_invoice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='invoice',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
