# Generated by Django 5.0.4 on 2024-05-13 12:28

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AudioTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('audio_file', models.FileField(upload_to='audio_tests/')),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category_images/')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('russian_word', models.CharField(max_length=100)),
                ('english_word', models.CharField(default='No translation provided', max_length=100)),
                ('distractors', models.CharField(default='Add words', max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='AudioQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
                ('correct_answer', models.CharField(max_length=255)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='website.audiotest')),
            ],
        ),
        migrations.AddField(
            model_name='audiotest',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='audio_tests', to='website.category'),
        ),
        migrations.CreateModel(
            name='ListeningTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video_url', models.URLField()),
                ('description', models.TextField(blank=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='video_tests', to='website.category')),
            ],
        ),
        migrations.CreateModel(
            name='ListeningQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_text', models.CharField(max_length=255)),
                ('correct_answer', models.CharField(max_length=255)),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='website.listeningtest')),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_question', models.IntegerField(default=0)),
                ('progress', models.IntegerField(default=0)),
                ('completed', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.category')),
                ('questions', models.ManyToManyField(to='website.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.word'),
        ),
    ]
