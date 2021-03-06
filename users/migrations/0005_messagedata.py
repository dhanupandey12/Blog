# Generated by Django 2.1.5 on 2019-08-22 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0004_profile_branch'),
    ]

    operations = [
        migrations.CreateModel(
            name='MessageData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('messageText', models.CharField(max_length=300)),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='SENDER', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
