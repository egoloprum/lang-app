# Generated by Django 4.1.6 on 2023-07-29 05:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_remove_selected_answer_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selected_answer',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quiz.answer'),
        ),
    ]
