# Generated by Django 2.2 on 2021-07-26 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swap_app', '0022_auto_20210726_0047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='gr_admin',
            field=models.ManyToManyField(default=None, related_name='admin_members', to='swap_app.User'),
        ),
    ]
