# Generated by Django 4.0.3 on 2022-12-17 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_remove_girdi_kategori_remove_girdi_sube_icmal_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grup',
            name='slug',
            field=models.SlugField(max_length=250),
        ),
    ]
