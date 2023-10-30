# Generated by Django 4.2.3 on 2023-10-25 22:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0004_alter_course_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='body',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='tag',
            field=models.CharField(blank=True, choices=[('Beginner', 'beginner'), ('Intermediate', 'intermediate'), ('Advanced', 'advanced')], default=None, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='topic',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='course_topic', to='course.topic'),
        ),
    ]