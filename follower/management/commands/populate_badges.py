import json
import os
import string
import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from user.models import Badge

class Command(BaseCommand):
   help = "Populate badges from a JSON file"

   def handle(self, *args, **options):
      with open("data/sample_badge.json", "r") as json_file:
         badge_data = json.load(json_file)
         created_badges = []

         for data in badge_data:
            badge_name = data['name']
            badge_description = data['description']
            badge_pts = data['pts']
            badge_exp = data['exp']
            badge_pic = f"badges/award-{random.randint(1, 3)}.jpg"

            try:
               host = User.objects.get(username='admin')
            except User.DoesNotExist:
               host = User.objects.create(username='admin', password='admin', is_superuser=True, is_staff=True)

            created = False

            try:
               badge = Badge.objects.get(host=host, name=badge_name, description=badge_description,
                                                         pts=badge_pts, exp=badge_exp)
               badge.picture = badge_pic
               badge.save()

            except Badge.DoesNotExist:
               badge = Badge.objects.create(host=host, name=badge_name, description=badge_description,
                                                         pts=badge_pts, exp=badge_exp, picture=badge_pic)
               created = True
            
            if created:
               self.stdout.write(
                  self.style.SUCCESS(f"Created badge: {badge.name}")
               )
               created_badges.append(badge.name)

            else:
               self.stdout.write(
                  self.style.WARNING(f"Badge already exists: {badge.name}")
               )
         
         self.stdout.write(
            self.style.SUCCESS(f"Successfully populated {len(created_badges)} badges")
         )

