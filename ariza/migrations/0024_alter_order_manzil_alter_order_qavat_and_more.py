# Generated by Django 4.2.3 on 2023-08-02 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ariza', '0023_order_tasdiqlash'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='manzil',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='order',
            name='qavat',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='order',
            name='yonalish',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]