# Generated by Django 4.2.3 on 2023-10-05 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0013_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='images/profile-picture/avatar.png', upload_to='photos/'),
        ),
    ]