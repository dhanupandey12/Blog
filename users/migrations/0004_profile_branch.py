# Generated by Django 2.1.5 on 2019-07-25 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_profile_enrollment'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='branch',
            field=models.CharField(default='CSE', max_length=3),
        ),
    ]
