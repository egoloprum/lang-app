# Generated by Django 3.2.8 on 2023-09-18 17:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0010_alter_content_body_alter_content_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='files',
        ),
        migrations.AddField(
            model_name='file',
            name='content',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.content'),
        ),
        migrations.AddField(
            model_name='file',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='course.course'),
        ),
    ]