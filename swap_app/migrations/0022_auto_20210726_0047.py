# Generated by Django 2.2 on 2021-07-26 00:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swap_app', '0021_group_active_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='active_group',
            field=models.CharField(max_length=3),
        ),
    ]