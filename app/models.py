from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import post_save


class UserProfile(models.Model):
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    user = models.OneToOneField(
        User, related_name='profile', primary_key=True, on_delete=models.CASCADE)

    slug = models.SlugField(
        max_length=1024, unique=True, blank=True, null=True)
    profile_image = models.URLField(max_length=2048, blank=True, null=True)
    description = models.TextField(max_length=160, blank=True, null=True)
    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers', blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        #! Disable if using python manage.py build_test_data command.
        if created:
            user_profile = UserProfile.objects.create(user=instance)
            user_profile.following.add(user_profile)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.user.username)
        super(UserProfile, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app:profile-detail-view', kwargs={'slug': self.slug})

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name} ({self.user.username})'


class Tag(models.Model):
    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"

    name = models.CharField(max_length=32, null=True)
    slug = models.SlugField(max_length=1024, blank=True,
                            unique=True, null=True)

    def get_absolute_url(self):
        return reverse('app:tag-detail-view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Post(models.Model):
    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    user_profile = models.ForeignKey(
        UserProfile, related_name='posts', null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=148, null=True)
    slug = models.SlugField(max_length=1024, blank=True,
                            unique=True, null=True)
    featured_image = models.URLField(max_length=2048, blank=True, null=True)
    content = models.TextField(max_length=64000, null=True)
    excerpt = models.TextField(max_length=480, null=True)
    tags = models.ManyToManyField(Tag, related_name='posts', blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def get_absolute_url(self):
        return reverse('app:post-detail-view', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.user_profile}: {self.title} ({self.slug})'
