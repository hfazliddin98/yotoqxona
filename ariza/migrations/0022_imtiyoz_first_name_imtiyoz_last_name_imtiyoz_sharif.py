# Generated by Django 4.2.2 on 2023-07-31 14:35

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ariza', '0021_rename_yillik_tolv_barcha_tolov_kiritish_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imtiyoz',
            name='first_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imtiyoz',
            name='last_name',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='imtiyoz',
            name='sharif',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
    ]
