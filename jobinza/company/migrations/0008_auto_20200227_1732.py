# Generated by Django 2.2.10 on 2020-02-27 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0007_auto_20200227_1720'),
    ]

    operations = [
        migrations.AlterField(
            model_name='createpost',
            name='deadline',
            field=models.DateTimeField(),
        ),
    ]
