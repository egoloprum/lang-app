# Generated by Django 4.2.3 on 2023-10-02 22:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='selected_answer',
            name='question',
            field=models.ForeignKey(null=False, on_delete=django.db.models.deletion.CASCADE, to='quiz.question'),
        ),
    ]