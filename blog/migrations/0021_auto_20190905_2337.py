# Generated by Django 2.1.5 on 2019-09-05 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0020_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='skills',
            field=models.ManyToManyField(default=None, to='blog.skillSet'),
        ),
    ]
