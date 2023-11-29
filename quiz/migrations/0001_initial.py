# Generated by Django 4.2.3 on 2023-11-06 19:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('course', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200)),
                ('correct', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.CharField(max_length=200)),
                ('explanation', models.CharField(blank=True, max_length=250, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pts', models.IntegerField(blank=True, default=0, null=True)),
                ('exp', models.IntegerField(blank=True, default=0, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('duration', models.TimeField(blank=True, help_text='duration of the quiz in minutes', null=True)),
                ('required_score', models.IntegerField(blank=True, default=60, help_text='required score in %', null=True)),
                ('difficulty', models.CharField(blank=True, max_length=50, null=True)),
                ('publication', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('content', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_content', to='course.content')),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_course', to='course.course')),
                ('host', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quiz_host', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('has_course', models.BooleanField(blank=True, null=True)),
                ('has_content', models.BooleanField(blank=True, null=True)),
                ('score', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_quiz', to='quiz.quiz')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='result_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Selected_Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sel_answer_ques', to='quiz.question')),
                ('result', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sel_answer_result', to='quiz.result')),
                ('selected', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sel_answer_ans', to='quiz.answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sel_answer_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_quiz', to='quiz.quiz'),
        ),
        migrations.CreateModel(
            name='Average_score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.FloatField()),
                ('question', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='average_score_ques', to='quiz.question')),
                ('quiz', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='average_score_quiz', to='quiz.quiz')),
                ('user', models.ManyToManyField(related_name='average_score_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='answer',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_question', to='quiz.question'),
        ),
    ]
