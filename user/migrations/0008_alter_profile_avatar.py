# Generated by Django 4.2.3 on 2023-10-05 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0007_profile_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='images/avatar.png', upload_to='static/images/profile-picture'),
        ),
    ]