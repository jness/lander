from django.contrib.auth.models import Group, User
from django.contrib.sites.models import Site

from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django_otp.plugins.otp_totp.models import TOTPDevice

from . import models


# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


# class TOTPDeviceSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = TOTPDevice

#         fields = [
#             'url', 'name', 'user', 'created_at', 'last_used_at', 'confirmed',
#             'throttling_failure_timestamp', 'throttling_failure_count', 'step',
#             't0', 'digits', 'tolerance', 'drift'
#         ]

#         read_only_fields = [
#             'created_at', 'last_used_at', 
#             'throttling_failure_timestamp', 'throttling_failure_count'
#         ]


# class TokenSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Token
#         fields = '__all__'


class SiteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Site
        fields = '__all__'


class TemplateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Template
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class LandingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Landing
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Article
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PriceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Price
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class TestimonialSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Testimonial
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Contact
        fields = '__all__'
        read_only_fields = [ i.name for i in models.Contact._meta.fields if i.name != 'responded']


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Schedule
        fields = '__all__'
        read_only_fields = ('last_success_at', 'last_failure_at')


class ScheduleLogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.ScheduleLog
        fields = '__all__'
        read_only_fields = ('created_at',)