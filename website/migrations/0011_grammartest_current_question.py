# Generated by Django 5.0.4 on 2024-05-13 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0010_rename_correct_word_grammarquestion_correct_answer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='grammartest',
            name='current_question',
            field=models.IntegerField(default=0),
        ),
    ]