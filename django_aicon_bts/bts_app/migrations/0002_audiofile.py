# Generated by Django 4.2.7 on 2023-11-26 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bts_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='audio_files/')),
            ],
        ),
    ]
