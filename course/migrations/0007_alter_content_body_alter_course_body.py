# Generated by Django 4.2.3 on 2023-08-16 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_alter_content_files'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='body',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='body',
            field=models.TextField(),
        ),
    ]
