# Generated by Django 4.2.3 on 2023-10-05 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_content_publication'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file',
            field=models.FileField(upload_to='media/files'),
        ),
    ]
