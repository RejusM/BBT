from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'nickname', 'city', 'country', 'gender')
    search_fields = ('nickname', 'first_name', 'last_name', 'city', 'country')


admin.site.register(UserProfile, UserProfileAdmin)
