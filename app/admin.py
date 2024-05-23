from django.conf import settings
from django.contrib import admin
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group

from django_summernote.admin import SummernoteModelAdmin
from django_summernote.models import Attachment
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_totp.models import TOTPDevice


from . import models 


# unregister so we can define layout
admin.site.unregister(Site)
admin.site.unregister(Group)
admin.site.unregister(StaticDevice)
#admin.site.unregister(Attachment)

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
    list_display = ["name", "path", "updated_at"]
    list_display_links = ["name"]
    search_fields = ["name", "path"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-updated_at"]

admin.site.register(models.Template, TemplateAdmin)


class LandingAdmin(admin.ModelAdmin):
    list_display = ["site", "updated_at", "enabled"]
    list_display_links = ["site"]
    list_filter = ["site__domain", "enabled"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-updated_at"]

admin.site.register(models.Landing, LandingAdmin)


class PriceAdmin(admin.ModelAdmin):
    list_display = ["site", "title", "cost", "updated_at", "featured", "enabled"]
    list_display_links = ["site"]
    list_filter = ["site__domain", "enabled"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-updated_at"]

admin.site.register(models.Price, PriceAdmin)


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ["site", "short_content", "updated_at", "enabled"]
    list_display_links = ["site"]
    list_filter = ["site__domain", "enabled"]
    readonly_fields = ["id", "created_at", "updated_at"]
    ordering = ["-updated_at"]

    def short_content(self, obj):
        "shorten content for display"
        return ' '.join(obj.content.split()[:20]) + "..."
    short_content.short_description = 'content'

admin.site.register(models.Testimonial, TestimonialAdmin)


class ArticleAdmin(SummernoteModelAdmin):
    list_display = ["site", "title", "author", "updated_at", "featured", "published"]
    list_display_links = ["site"]
    list_filter = ["site__domain", "featured", "published"]
    readonly_fields = ["id", "slug_name", "created_at", "updated_at"]
    ordering = ["-updated_at"]

    summernote_fields = ('content',)

admin.site.register(models.Article, ArticleAdmin)


class ContactAdmin(admin.ModelAdmin):
    list_display = ["site", "full_name", "message_short", "updated_at", "responded"]
    list_display_links = ["site"]
    list_filter = ["site__domain", "responded"]
    readonly_fields = [ i.name for i in models.Contact._meta.fields ]  # make all fields readonly
    ordering = ["-updated_at"]

    def message_short(self, obj):
        "shorten comment for display"
        return ' '.join(obj.message.split()[:20]) + '...'
    message_short.short_description = 'message'

admin.site.register(models.Contact, ContactAdmin)


class ScheduleAdmin(admin.ModelAdmin):
    list_display = ["name", "command", "updated_at", "last_success_at", "last_failure_at", "enabled"]
    list_display_links = ["name"]
    search_fields = ["name", "command"]
    list_filter = ["command", "enabled"]
    readonly_fields = ["id", "created_at", "updated_at", "last_success_at", "last_failure_at"]
    ordering = ["-updated_at"]

if settings.CRON_SCHEDULES:
    admin.site.register(models.Schedule, ScheduleAdmin)


class ScheduleLogAdmin(admin.ModelAdmin):
    list_display = ["schedule", "content", "updated_at"]
    list_display_links = ["schedule"]
    search_fields = ["schedule__name", "content"]
    readonly_fields = ["id", "schedule", "content", "created_at", "updated_at"]
    ordering = ["-updated_at"]

if settings.CRON_SCHEDULES:
    admin.site.register(models.ScheduleLog, ScheduleLogAdmin)
