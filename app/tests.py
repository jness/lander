import os

from django.conf import settings
from django.test import Client
from django.test import TestCase

from . import models


class SettingsTestCase(TestCase):

    def test_settings(self):
        """
        Test for settings.py
        """

        self.assertFalse(settings.DEBUG)
        self.assertTrue(settings.OTP_ENABLED)
        self.assertEqual(settings.PRIMARY_SITE, settings.SITE_ID)


class TemplateTestCase(TestCase):

    fixtures = ('app/fixtures/initial_data.json',)

    def setUp(self):
        pass

    def test_model_template(self):
        """
        Test for the Template Model
        """

        obj = models.Template.objects.get(id=1)

        self.assertEqual(obj.name, 'one_page_wonder')
        self.assertEqual(obj.path, 'app/one_page_wonder.html')

        # ensure the template file exist in templates path
        _file = os.path.join(os.path.abspath('.'), 'templates/' + obj.path)
        self.assertTrue(_file)

    def test_view_template(self):
        """
        Test the template render properly for each site
        """

        client = Client()

        # check proper navbar name for site
        response = client.get("/", headers={'Host': 'django-tacos.com'})
        navbar = '<a class="navbar-brand" href="/">django-tacos</a>'
        self.assertTrue(navbar in str(response.content))

        # check proper navbar name for site
        response = client.get("/", headers={'Host': 'django-burgers.com'})
        navbar = '<a class="navbar-brand" href="/">django-burgers</a>'
        self.assertTrue(navbar in str(response.content))
