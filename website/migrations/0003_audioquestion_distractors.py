# Generated by Django 5.0.4 on 2024-05-13 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0002_remove_audiotest_audio_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='audioquestion',
            name='distractors',
            field=models.CharField(default='Add words', max_length=300),
        ),
    ]