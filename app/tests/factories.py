"""
IMPORTS
"""
import factory

from faker import Faker
fake = Faker()

from django.contrib.auth.models import User
from .. import models

import random

"""
FACTORIES
"""
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.LazyAttribute(lambda o: fake.unique.user_name())
    password = factory.PostGenerationMethodCall('set_password', 'testpassword')
    email = factory.LazyAttribute(lambda o: fake.unique.email())
    first_name = factory.LazyAttribute(lambda o: fake.first_name())
    last_name = factory.LazyAttribute(lambda o: fake.last_name())

class CreatorProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.CreatorProfile
        django_get_or_create = ('user',)

    user = factory.SubFactory(UserFactory)
    slug = factory.LazyAttribute(lambda o: fake.unique.slug())
    profile_image = factory.LazyAttribute(lambda o: fake.image_url(170, 170))
    description = factory.LazyAttribute(lambda o: fake.text())
    date_created = factory.LazyAttribute(lambda o: fake.date_time())

class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tag

    name = factory.LazyAttribute(lambda o: fake.unique.word())
    slug = factory.LazyAttribute(lambda o: fake.unique.slug())

class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Post

    creator_profile = factory.Iterator(models.CreatorProfile.objects.all())
    title = factory.LazyAttribute(lambda o: fake.unique.sentence())
    slug = factory.LazyAttribute(lambda o: fake.slug())
    featured_image = factory.LazyAttribute(lambda o: fake.image_url(1920, 1080))
    content = factory.LazyAttribute(lambda o: fake.paragraph(nb_sentences=120))
    excerpt = factory.LazyAttribute(lambda o: fake.text())