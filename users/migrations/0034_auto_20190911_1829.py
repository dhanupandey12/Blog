# Generated by Django 2.1.5 on 2019-09-11 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_auto_20190911_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='OTP',
            field=models.IntegerField(default=907332),
        ),
    ]
