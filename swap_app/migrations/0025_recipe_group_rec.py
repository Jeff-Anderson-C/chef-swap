# Generated by Django 2.2 on 2021-07-27 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('swap_app', '0024_invite'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='group_rec',
            field=models.ManyToManyField(related_name='group_recs', to='swap_app.Group'),
        ),
    ]