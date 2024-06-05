from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from django_summernote.admin import SummernoteModelAdmin
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_totp.models import TOTPDevice


from . import models 


# unregister so we can define layout
admin.site.unregister(Site)
admin.site.unregister(Group)
admin.site.unregister(StaticDevice)


# remove OTP models if disabled
if not settings.OTP_ENABLED:
    admin.site.unregister(TOTPDevice)


class SiteAdmin(admin.ModelAdmin):
    list_display = ["name", "domain"]
    list_display_links = ["name"]
    search_fields = ["name", "domain"]
    readonly_fields = ["id"]
    ordering = ["id"]

admin.site.register(Site, SiteAdmin)


class TemplateAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "path", "created_at", "updated_at"]
    list_display_links = ["id"]
    search_fields = ["name", "path"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-created_at"]

admin.site.register(models.Template, TemplateAdmin)


class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    list_display_links = ["name"]
    search_fields = ["name"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-created_at"]

admin.site.register(models.Tag, TagAdmin)


class LandingAdmin(SummernoteModelAdmin):
    list_display = ["site", "page_title", "created_at", "updated_at", "enabled"]
    list_display_links = ["site"]
    list_filter = ["site__domain", "enabled"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-created_at"]

    summernote_fields = ('about',)

admin.site.register(models.Landing, LandingAdmin)


class ArticleAdmin(SummernoteModelAdmin):
    list_display = ["title", "site", "author", "tag_names", "created_at", "updated_at",  "published"]
    list_display_links = ["title"]
    list_filter = ["site__domain", "tags", "published"]
    readonly_fields = ["id", "slug_name", "created_at", "updated_at"]
    ordering = ["-created_at"]
    filter_horizontal = ["tags",]

    summernote_fields = ('content',)

    def tag_names(self, obj):
        "List of tag names"
        return [ i['name'] for i in obj.tags.values() ]
    tag_names.short_description = 'tags'

admin.site.register(models.Article, ArticleAdmin)


class ArticleBotAdmin(SummernoteModelAdmin):
    list_display = ["name", "site", "created_at", "updated_at", "enabled"]
    list_display_links = ["name"]
    list_filter = ["site__domain", "enabled"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-created_at"]

admin.site.register(models.ArticleBot, ArticleBotAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ["email", "full_name", "message_short", "site", "created_at", "updated_at", "responded"]
    list_display_links = ["email"]
    list_filter = ["site__domain", "responded"]
    readonly_fields = [ i.name for i in models.Contact._meta.fields if i.name != "responded" ]  # make all fields readonly
    ordering = ["-created_at"]

    def message_short(self, obj):
        "shorten comment for display"
        return ' '.join(obj.message.split()[:20]) + '...'
    message_short.short_description = 'message'

admin.site.register(models.Contact, ContactAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["name", "command", "created_at", "updated_at", "last_success_at", "last_failure_at", "enabled"]
    list_display_links = ["name"]
    search_fields = ["name", "command"]
    list_filter = ["command", "enabled"]
    readonly_fields = ["id", "created_at", "updated_at", "last_success_at", "last_failure_at"]
    ordering = ["-created_at"]

if settings.CRON_SCHEDULES:
    admin.site.register(models.Schedule, ScheduleAdmin)


class ScheduleLogAdmin(admin.ModelAdmin):
    list_display = ["schedule", "content", "created_at", "updated_at"]
    list_display_links = ["schedule"]
    search_fields = ["schedule__name", "content"]
    readonly_fields = ["id", "schedule", "content", "created_at", "updated_at"]
    ordering = ["-created_at"]

if settings.CRON_SCHEDULES:
    admin.site.register(models.ScheduleLog, ScheduleLogAdmin)
