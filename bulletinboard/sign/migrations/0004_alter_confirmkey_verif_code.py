# Generated by Django 4.0.5 on 2022-10-29 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0003_alter_confirmkey_verif_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmkey',
            name='verif_code',
            field=models.CharField(default=0, max_length=6, unique=True),
        ),
    ]
