import json
import string
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = "Populates users from a JSON file"

    def handle(self, *args, **options):
      User = get_user_model()
      created_users = []

      for x in range(0, 20):
        username = "account" + str(x)
        username_admin = "admin" + str(x)
        password = "Qawsedrf12"

        user, created = User.objects.get_or_create(
          username=username, password=password
        )

        admin, created_admin = User.objects.get_or_create(
           username=username_admin, password=password, is_superuser=True, is_staff=True, is_active=True
        )

        if created or created_admin:
           self.stdout.write(
              self.style.SUCCESS(f"Created user: {user.username} and admin: {admin.username}")
           )
           created_users.append(user.username)
        else:
          self.stdout.write(
             self.style.WARNING(f"User already exists: {user.username} and admin: {admin.username}")
          )

      self.stdout.write(
         self.style.SUCCESS(f"successfully populated {len(created_users)} users")
      )

