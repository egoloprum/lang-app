import json
import random
import datetime
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

from user.models import Profile, Badge
from follower.models import NotificationList

class Command(BaseCommand):
   help = "Populates users from a JSON file"

   def handle(self, *args, **options):
      User = get_user_model()
      created_users = []

      fake = Faker()
      fake_usernames = []

      for _ in range(30):
         fake_usernames.append(fake.first_name())

      fake_usernames = list(set(fake_usernames))

      for x in range(0, 20):
         username = fake_usernames[x]
         username_staff = 'staff' + str(x)
         password = "Qawsedrf12"
         password = make_password(password)
      
         try:
            User.objects.get(username=username).delete()
         except Exception:
            ...

         try:
            User.objects.get(username=username_staff).delete()
         except Exception:
            ...

         user, created = User.objects.get_or_create(
            username=username, password=password
         )

         try:
            Profile.objects.get(user=user)
         except Profile.DoesNotExist:
            profile = Profile.objects.create(user=user, birthday=fake.date_between(end_date=datetime.date(2010, 1, 1)), 
                                             gender=fake.profile()['sex'], country=fake.country(),
                                             level=random.randint(1, 10))
            profile_level = profile.level
            profile.experience = profile_level * 500
            profile.badge.add(Badge.objects.get(name='Welcome to English Study'))
            profile.save()

         try:
            NotificationList.objects.get(user=user)
         except NotificationList.DoesNotExist:
            NotificationList.objects.create(user=user)

         staff, created_staff = User.objects.get_or_create(
            username=username_staff, password=password, is_staff=True, is_active=True
         )

         try:
            Profile.objects.get(user=staff)
         except Profile.DoesNotExist:
            profile = Profile.objects.create(user=staff, birthday=fake.date_between(end_date=datetime.date(2010, 1, 1)),
                                             gender=fake.profile()['sex'], country=fake.country(),
                                             level=random.randint(1, 10))
            profile.badge.add(Badge.objects.get(name='Welcome to English Study'))
            profile.save()

         try:
            NotificationList.objects.get(user=staff)
         except NotificationList.DoesNotExist:
            NotificationList.objects.create(user=staff)

         if created or created_staff:
            self.stdout.write(
               self.style.SUCCESS(f"Created user: {user.username} and admin: {staff.username}")
            )
            created_users.append(user.username)
         else:
            self.stdout.write(
               self.style.WARNING(f"User already exists: {user.username} and admin: {staff.username}")
            )

      self.stdout.write(
         self.style.SUCCESS(f"successfully populated {len(created_users)} users")
      )

