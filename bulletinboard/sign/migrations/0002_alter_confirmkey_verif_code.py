# Generated by Django 4.0.5 on 2022-10-29 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sign', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='confirmkey',
            name='verif_code',
            field=models.CharField(default=445395, max_length=6, unique=True),
        ),
    ]