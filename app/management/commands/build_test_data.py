"""
IMPORTS
"""
import random
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import *
from ...tests.factories import *

"""
SIZE
"""
NUM_CREATOR_PROFILES = 50
NUM_POSTS = 100
NUM_TAGS = 100

"""
COMMAND
"""
class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, CreatorProfile, Post, Tag]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_CREATOR_PROFILES):
            creator_profile = CreatorProfileFactory()
            all_creator_profile = CreatorProfile.objects.all()
            random_number = random.randint(0, len(all_creator_profile))
            _creator_profiles = random.choices(all_creator_profile, k=random_number)
            _creator_profiles.append(creator_profile)
            creator_profile.following.add(*_creator_profiles)  

        for _ in range(NUM_TAGS):
            tags = TagFactory()

        for _ in range(NUM_POSTS):
            posts = PostFactory()
            all_tags = Tag.objects.all()
            random_number = random.randint(0, 15)
            _tags = random.choices(all_tags, k=random_number)
            posts.tags.add(*_tags)