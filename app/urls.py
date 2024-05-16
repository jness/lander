from django.conf import settings
from django.urls import path, include
from django.contrib import admin

from rest_framework import routers

from . import views
from . import api


# register api views
router = routers.DefaultRouter()
# router.register(r"users", api.UserViewSet)
# router.register(r"groups", api.GroupViewSet)
# router.register(r"totp_devices", api.TOTPDeviceViewSet)
# router.register(r"api_tokens", api.TokenViewSet)
router.register(r"sites", api.SiteViewSet)
router.register(r"templates", api.TemplateViewSet)
router.register(r"landings", api.LandingViewSet)
router.register(r"articles", api.ArticleViewSet)
router.register(r"prices", api.PriceViewSet)
router.register(r"testimonials", api.TestimonialViewSet)
router.register(r"contacts", api.ContactViewSet)

if settings.CRON_SCHEDULES:
    router.register(r"schedules", api.ScheduleViewSet)
    router.register(r"schedule_logs", api.ScheduleLogViewSet)

# define app urls paths
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path('summernote/', include('django_summernote.urls')),
    path("", views.index, name="index"),
]
