# Generated by Django 2.2 on 2021-07-25 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swap_app', '0020_auto_20210725_2205'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='active_group',
            field=models.BooleanField(default=True),
        ),
    ]