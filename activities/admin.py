from django.contrib import admin
from .models import User, Activity, Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('nom')


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title', 'location_city', 'start_time', 'end_time', 'proposer')
    list_filter = ('location_city', 'start_time', 'end_time', 'category')
    search_fields = ('title', 'description', 'location_city', 'proposer__username', 'category__nom')
    filter_horizontal = ('attendees',)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('username', 'email')
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(User)
admin.site.register(Activity)
admin.site.register(Category)
# Register your models here.
