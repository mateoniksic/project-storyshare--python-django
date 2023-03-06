# Generated by Django 4.1.3 on 2023-02-21 16:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('app', '0004_remove_creatorprofile_followers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('slug', models.SlugField(blank=True, max_length=1024, null=True, unique=True)),
                ('profile_image', models.URLField(blank=True, max_length=2048, null=True)),
                ('description', models.TextField(blank=True, max_length=160, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('following', models.ManyToManyField(blank=True, related_name='followers', to='app.userprofile')),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
        migrations.RemoveField(
            model_name='post',
            name='creator_profile',
        ),
        migrations.DeleteModel(
            name='CreatorProfile',
        ),
        migrations.AddField(
            model_name='post',
            name='user_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='app.userprofile'),
        ),
    ]