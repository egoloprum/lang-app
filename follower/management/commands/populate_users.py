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
        password = "Qawsedrf12"

        user, created = User.objects.get_or_create(
          username=username, password=password
        )

        if created:
           self.stdout.write(
              self.style.SUCCESS(f"Created user: {user.username}")
           )
           created_users.append(user.username)
        else:
          self.stdout.write(
             self.style.WARNING(f"User already exists: {user.username}")
          )

      self.stdout.write(
         self.style.SUCCESS(f"successfully populated {len(created_users)} users")
      )

