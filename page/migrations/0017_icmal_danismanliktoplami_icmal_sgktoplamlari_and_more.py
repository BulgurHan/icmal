# Generated by Django 4.0.3 on 2022-12-25 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0016_remove_girdi_konu_remove_girdi_tutar_girdi_bagkur_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='icmal',
            name='danismanliktoplami',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='sgktoplamlari',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='vergilertoplami',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11, null=True),
        ),
    ]
