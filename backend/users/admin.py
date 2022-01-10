from django.conf import settings
from django.contrib import admin

from .models import Subscription, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'first_name', 'last_name', 'email')
    search_fields = ('first_name',)
    empty_value_display = '-пусто-'


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('subscriber', 'subscription')
    search_fields = ('subscriber',)
    list_filter = ('subscription',)
    empty_value_display = settings.BLANK_VALUE_CONST
