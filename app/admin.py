from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import *


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    readonly_fields = ('slug',)
    can_delete = False


class AccountsUserAdmin(UserAdmin):
    def add_view(self, *arg, **kwargs):
        self.inlines = []
        return super(UserAdmin, self).add_view(*arg, **kwargs)

    def change_view(self, *arg, **kwargs):
        self.inlines = [UserProfileInline]
        return super(UserAdmin, self).change_view(*arg, **kwargs)


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


class TagAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)


unregister_models_list = [
    User,
]

register_models_list = [
    Post,
    Tag,
]

admin.site.unregister(unregister_models_list)

admin.site.register(User, AccountsUserAdmin)
admin.site.register(register_models_list)
