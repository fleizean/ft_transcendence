# Generated by Django 4.2.3 on 2024-02-13 17:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pong', '0013_alter_storeitem_category_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournamentmatch',
            name='loserscore',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='tournamentmatch',
            name='winnerscore',
            field=models.IntegerField(default=0),
        ),
    ]
