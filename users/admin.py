from django.contrib import admin

from users.models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'first_name', 'last_name', 'phone', 'email', 'role')
    list_filter = ('email', 'last_name',)
    search_fields = ('email',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'date_of_birth', 'registration_date',)
    list_filter = ('user', 'registration_date',)
