# Generated by Django 5.0 on 2024-01-07 15:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pong', '0005_userprofile_online'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='status',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='channel_name',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='online',
        ),
    ]
