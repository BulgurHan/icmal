# Generated by Django 4.0.3 on 2022-12-18 12:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0009_remove_girdi_personel'),
    ]

    operations = [
        migrations.AddField(
            model_name='icmal',
            name='bagkur',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='ceza',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='damga',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='davagideri',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='gecmismüsavirlik',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='gecmistesvik',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='geçmişborçlar',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='ggkv',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='hakemheyeti',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='harcama',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='idariceza',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='kdv',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='kdv2',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='mtv',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='muhtasar',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='müsavirlik',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='sgk',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
        migrations.AddField(
            model_name='icmal',
            name='tesvik',
            field=models.DecimalField(decimal_places=2, max_digits=11, null=True),
        ),
    ]
