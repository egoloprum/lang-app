# Generated by Django 4.2.3 on 2023-11-04 12:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('follower', '0004_alter_chatroom_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receiver', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NotificationList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='list_notification', to='follower.notification')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='list_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]