# Generated by Django 4.2.3 on 2023-10-10 23:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_selected_answer_result_alter_result_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selected_answer',
            name='result',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, related_name='sel_answer_result', to='quiz.result'),
        ),
    ]
