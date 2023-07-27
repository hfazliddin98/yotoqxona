# Generated by Django 4.2.2 on 2023-07-26 18:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ariza', '0018_alter_order_talaba_id_alter_rasm_talaba_id_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_link',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('talaba_id', models.CharField(max_length=100)),
                ('link', models.CharField(blank=True, max_length=100)),
                ('rasm', models.FileField(upload_to='order_qrcode/')),
            ],
        ),
    ]
