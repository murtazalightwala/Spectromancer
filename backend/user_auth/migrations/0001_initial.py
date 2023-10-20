# Generated by Django 4.2.6 on 2023-10-17 22:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('special', models.CharField(choices=[('death', 'Death'), ('chaos', 'Chaos')], max_length=40)),
                ('avatar_url', models.URLField()),
                ('mobile_number', models.CharField(max_length=15)),
            ],
            options={
                'db_table': 'user_profile',
            },
        ),
    ]
