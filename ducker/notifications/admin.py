from django.contrib import admin

from .models import (
    FollowUpEvent,
    Medium,
    NotificationEvent,
    NotificationHistory,
    OneTimeNotifyEvent,
)


class FollowupEventInlineAdmin(admin.StackedInline):
    model = FollowUpEvent
    fk_name = "after_event"
    extra = 1


@admin.register(Medium)
class MediumAdmin(admin.ModelAdmin):
    list_display = ("label", "slug", "text_format")


@admin.register(NotificationEvent)
class NotificationEventAdmin(admin.ModelAdmin):
    inlines = (FollowupEventInlineAdmin,)
    list_display = ("label", "identifier", "is_active")


@admin.register(NotificationHistory)
class NotificationHistoryAdmin(admin.ModelAdmin):
    list_display = ("event", "user", "ref_id", "created_at")


@admin.register(OneTimeNotifyEvent)
class OneTimeNotifyEventAdmin(admin.ModelAdmin):
    pass
