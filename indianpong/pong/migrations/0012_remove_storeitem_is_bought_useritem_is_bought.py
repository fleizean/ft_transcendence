# Generated by Django 5.0 on 2024-02-12 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pong', '0011_rename_is_status_storeitem_show_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storeitem',
            name='is_bought',
        ),
        migrations.AddField(
            model_name='useritem',
            name='is_bought',
            field=models.BooleanField(default=False),
        ),
    ]
