# Generated by Django 5.0 on 2024-02-10 00:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pong', '0002_alter_userprofile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(blank=True, max_length=200, null=True)),
                ('product_description', models.CharField(blank=True, max_length=200, null=True)),
                ('product_price', models.IntegerField(blank=True, null=True)),
                ('product_buystatus', models.BooleanField(default=False)),
                ('product_status', models.BooleanField(default=True)),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='pong_wallet',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='store',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='pong.store'),
        ),
    ]