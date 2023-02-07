# Generated by Django 4.0.3 on 2023-02-01 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='firma',
            options={'ordering': ('isim',)},
        ),
        migrations.AlterModelOptions(
            name='firmaicmal',
            options={'ordering': ('-yıl',)},
        ),
        migrations.AlterModelOptions(
            name='icmal',
            options={'ordering': ('-yıl',)},
        ),
        migrations.AlterField(
            model_name='firmaicmal',
            name='ay',
            field=models.IntegerField(choices=[(1, 1)], default=2, verbose_name='ay'),
        ),
        migrations.AlterField(
            model_name='firmaicmal',
            name='yıl',
            field=models.IntegerField(choices=[(2023, 2023)], default=2023, verbose_name='yıl'),
        ),
        migrations.AlterField(
            model_name='grupicmal',
            name='ay',
            field=models.IntegerField(choices=[(1, 1)], default=2, verbose_name='ay'),
        ),
        migrations.AlterField(
            model_name='grupicmal',
            name='yıl',
            field=models.IntegerField(choices=[(2023, 2023)], default=2023, verbose_name='yıl'),
        ),
        migrations.AlterField(
            model_name='icmal',
            name='ay',
            field=models.IntegerField(choices=[(1, 1)], default=2, verbose_name='ay'),
        ),
        migrations.AlterField(
            model_name='icmal',
            name='yıl',
            field=models.IntegerField(choices=[(2023, 2023)], default=2023, verbose_name='yıl'),
        ),
    ]
