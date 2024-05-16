from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

from rest_framework import permissions, viewsets
from rest_framework.authtoken.models import Token
from django_otp.plugins.otp_totp.models import TOTPDevice

from . import serializers
from . import models


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = serializers.UserSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all().order_by('name')
#     serializer_class = serializers.GroupSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class TOTPDeviceViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = TOTPDevice.objects.all()
#     serializer_class = serializers.TOTPDeviceSerializer
#     permission_classes = [permissions.IsAuthenticated]


# class TokenViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Token.objects.all()
#     serializer_class = serializers.TokenSerializer
#     permission_classes = [permissions.IsAuthenticated]


class SiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows sites to be viewed or edited.
    """
    queryset = Site.objects.all()
    serializer_class = serializers.SiteSerializer
    permission_classes = [permissions.IsAuthenticated]


class TemplateViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows templates to be viewed or edited.
    """
    queryset = models.Template.objects.all()
    serializer_class = serializers.TemplateSerializer
    permission_classes = [permissions.IsAuthenticated]


class LandingViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows landings to be viewed or edited.
    """
    queryset = models.Landing.objects.all()
    serializer_class = serializers.LandingSerializer
    permission_classes = [permissions.IsAuthenticated]


class ArticleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows landings to be viewed or edited.
    """
    queryset = models.Article.objects.all()
    serializer_class = serializers.ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]


class PriceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows templates to be viewed or edited.
    """
    queryset = models.Price.objects.all()
    serializer_class = serializers.PriceSerializer
    permission_classes = [permissions.IsAuthenticated]


class TestimonialViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows templates to be viewed or edited.
    """
    queryset = models.Testimonial.objects.all()
    serializer_class = serializers.TestimonialSerializer
    permission_classes = [permissions.IsAuthenticated]


class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows templates to be viewed or edited.
    """
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScheduleViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows templates to be viewed or edited.
    """
    queryset = models.Schedule.objects.all()
    serializer_class = serializers.ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

class ScheduleLogViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows templates to be viewed or edited.
    """
    queryset = models.ScheduleLog.objects.all()
    serializer_class = serializers.ScheduleLogSerializer
    permission_classes = [permissions.IsAuthenticated]