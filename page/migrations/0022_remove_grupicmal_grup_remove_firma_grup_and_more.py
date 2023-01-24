# Generated by Django 4.0.3 on 2023-01-07 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0021_firmaicmal_cezalar_firmaicmal_digercezalar_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grupicmal',
            name='grup',
        ),
        migrations.RemoveField(
            model_name='firma',
            name='grup',
        ),
        migrations.AlterField(
            model_name='firmaicmal',
            name='ay',
            field=models.IntegerField(choices=[(12, 12)], default=1, verbose_name='ay'),
        ),
        migrations.AlterField(
            model_name='firmaicmal',
            name='yıl',
            field=models.IntegerField(choices=[(2022, 2022)], default=2023, verbose_name='yıl'),
        ),
        migrations.AlterField(
            model_name='girdi',
            name='ay',
            field=models.IntegerField(choices=[(12, 12)], default=1, verbose_name='ay'),
        ),
        migrations.AlterField(
            model_name='girdi',
            name='yıl',
            field=models.IntegerField(choices=[(2022, 2022)], default=2023, verbose_name='yıl'),
        ),
        migrations.AlterField(
            model_name='icmal',
            name='ay',
            field=models.IntegerField(choices=[(12, 12)], default=1, verbose_name='ay'),
        ),
        migrations.AlterField(
            model_name='icmal',
            name='yıl',
            field=models.IntegerField(choices=[(2022, 2022)], default=2023, verbose_name='yıl'),
        ),
        migrations.DeleteModel(
            name='Grup',
        ),
        migrations.DeleteModel(
            name='GrupIcmal',
        ),
    ]
