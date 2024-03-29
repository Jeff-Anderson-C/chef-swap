# Generated by Django 2.2 on 2021-07-26 23:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swap_app', '0023_auto_20210726_0058'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('msg_txt', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('for_group', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='swap_app.Group')),
                ('sender', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='swap_app.User')),
            ],
        ),
    ]
