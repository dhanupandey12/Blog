# Generated by Django 2.1.5 on 2019-09-10 10:22

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0024_new'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='New',
            new_name='FriendTable',
        ),
        migrations.RenameField(
            model_name='friendtable',
            old_name='friendsData',
            new_name='friends',
        ),
    ]
