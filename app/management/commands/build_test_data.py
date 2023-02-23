import random
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import *
from ...tests.factories import *


NUM_CREATOR_PROFILES = 50
NUM_POSTS = 250
NUM_TAGS = 50


class Command(BaseCommand):
    help = "Generates test data"

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write("Deleting old data...")
        models = [User, UserProfile, Post, Tag]
        for m in models:
            m.objects.all().delete()

        self.stdout.write("Creating new data...")

        for _ in range(NUM_CREATOR_PROFILES):
            creator_profile = UserProfileFactory()
            user_profiles_all = UserProfile.objects.all()
            random_number = random.randint(0, len(user_profiles_all))
            _user_profiles = random.choices(
                user_profiles_all, k=random_number)
            _user_profiles.append(creator_profile)
            creator_profile.followers.add(*_user_profiles)

        for _ in range(NUM_TAGS):
            tags = TagFactory()

        for _ in range(NUM_POSTS):
            posts = PostFactory()
            all_tags = Tag.objects.all()
            random_number = random.randint(0, 15)
            _tags = random.choices(all_tags, k=random_number)
            posts.tags.add(*_tags)
