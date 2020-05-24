# Generated by Django 2.1.5 on 2019-09-05 18:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0022_auto_20190905_2343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='likeonpost',
            options={},
        ),
        migrations.AddField(
            model_name='likeonpost',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='likeonpost',
            name='post',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='blog.Post'),
        ),
        migrations.AlterUniqueTogether(
            name='likeonpost',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='likeonpost',
            name='likeCount',
        ),
        migrations.RemoveField(
            model_name='likeonpost',
            name='user',
        ),
    ]