# Generated by Django 2.1.5 on 2019-08-28 07:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_friends'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='friends',
            options={'verbose_name': 'Friend List', 'verbose_name_plural': 'Friend List'},
        ),
        migrations.AlterModelOptions(
            name='messagedata',
            options={'verbose_name': 'Messages', 'verbose_name_plural': 'Messages'},
        ),
        migrations.RenameField(
            model_name='friends',
            old_name='friends',
            new_name='friendList',
        ),
    ]