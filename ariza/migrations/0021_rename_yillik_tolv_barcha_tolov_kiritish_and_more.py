# Generated by Django 4.2.2 on 2023-07-27 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ariza', '0020_rename_hisob_raqam_barcha_tolov_ttj_soni_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='barcha_tolov',
            old_name='yillik_tolv',
            new_name='kiritish',
        ),
        migrations.AddField(
            model_name='barcha_tolov',
            name='yillik_tolov',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]
