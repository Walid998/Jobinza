# Generated by Django 2.2.10 on 2020-02-27 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0009_auto_20200227_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createpost',
            name='deadline',
            field=models.DateField(),
        ),
    ]
