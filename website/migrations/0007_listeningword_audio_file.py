# Generated by Django 5.0.4 on 2024-05-13 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0006_alter_listeningtest_questions'),
    ]

    operations = [
        migrations.AddField(
            model_name='listeningword',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to='listening_words/'),
        ),
    ]