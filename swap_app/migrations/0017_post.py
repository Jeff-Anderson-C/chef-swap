# Generated by Django 2.2 on 2021-07-23 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('swap_app', '0016_auto_20210723_0111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('post_title', models.CharField(max_length=45)),
                ('content', models.CharField(max_length=455)),
                ('post_image', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='swap_app.Image')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]