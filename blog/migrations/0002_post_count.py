# Generated by Django 2.1.5 on 2019-08-22 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='count',
            field=models.IntegerField(default=1),
        ),
    ]
