# Generated by Django 2.1.5 on 2019-08-26 03:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_messagedata_sendername'),
    ]

    operations = [
        migrations.AddField(
            model_name='messagedata',
            name='seen',
            field=models.BooleanField(default=True),
        ),
    ]