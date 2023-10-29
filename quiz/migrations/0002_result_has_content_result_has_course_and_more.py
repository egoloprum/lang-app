# Generated by Django 4.2.3 on 2023-10-28 21:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='result',
            name='has_content',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='result',
            name='has_course',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='quiz',
            name='required_score',
            field=models.IntegerField(blank=True, default=60, help_text='required score in %', null=True),
        ),
    ]
