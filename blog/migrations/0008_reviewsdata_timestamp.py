# Generated by Django 2.1.5 on 2019-08-23 15:59

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_reviewsdata'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviewsdata',
            name='timeStamp',
            field=models.DateTimeField(default=datetime.datetime(2019, 8, 23, 15, 59, 39, 740611, tzinfo=utc)),
        ),
    ]
