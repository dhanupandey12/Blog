# Generated by Django 2.1.5 on 2019-09-12 09:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0035_auto_20190912_1434'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.AlterField(
            model_name='profile',
            name='OTP',
            field=models.IntegerField(default=423395),
        ),
    ]