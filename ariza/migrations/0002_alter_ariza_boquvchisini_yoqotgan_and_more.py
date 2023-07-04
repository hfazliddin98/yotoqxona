from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ariza', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ariza',
            name='boquvchisini_yoqotgan',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='ariza',
            name='chin_yetim',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='ariza',
            name='daftar_turishi',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='ariza',
            name='nogironlig',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
