# Generated by Django 4.1.6 on 2023-08-12 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_remove_followrequest_reciever_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='badges',
            field=models.ManyToManyField(blank=True, to='user.badge'),
        ),
    ]
