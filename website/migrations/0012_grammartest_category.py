# Generated by Django 5.0.4 on 2024-05-13 21:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_grammartest_current_question'),
    ]

    operations = [
        migrations.AddField(
            model_name='grammartest',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.category'),
        ),
    ]
