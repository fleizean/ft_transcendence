# Generated by Django 5.0 on 2024-01-03 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pong', '0003_rename_matchhistory_matchrecord_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='channel_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
