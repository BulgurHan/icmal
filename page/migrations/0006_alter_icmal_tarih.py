# Generated by Django 4.0.3 on 2022-12-18 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0005_remove_icmal_girdi_icmal_toplam_icmalitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='icmal',
            name='tarih',
            field=models.DateField(auto_now_add=True),
        ),
    ]
