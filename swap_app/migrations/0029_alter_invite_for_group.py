# Generated by Django 3.2.5 on 2021-07-31 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swap_app', '0028_auto_20210730_2151'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='for_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='swap_app.group'),
        ),
    ]
