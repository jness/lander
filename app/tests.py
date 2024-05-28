import os

from django.conf import settings
from django.test import Client
from django.test import TestCase
from django.contrib.sites.models import Site

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


class LandingTestCase(TestCase):

    fixtures = ('app/fixtures/initial_data.json',)

    def setUp(self):
        self.primary_site = Site.objects.get(domain='django-tacos.com')
        self.secondary_site = Site.objects.get(domain='django-burgers.com')

    def test_model_landing(self):
        """
        Test for the Landing Model
        """

        # test for primary site
        obj = models.Landing.objects.get(id=1)
        self.assertEqual(obj.page_title, 'Delicious Tacos')
        self.assertEqual(obj.site, self.primary_site)

        # test for secondary site
        obj = models.Landing.objects.get(id=2)
        self.assertEqual(obj.page_title, 'Delicious Burgers')
        self.assertEqual(obj.site, self.secondary_site)

    def test_multiple_landing_same_site(self):
        """
        Test for the multiple Landings referencing same site
        """

        # create new landing object tied to existing primary site
        obj = models.Landing(
            page_title = 'Another one',
            site = self.primary_site
        )

        # ensure we get exception when saving
        self.assertRaisesMessage(
            Exception, 'Landing for site already exists.', obj.save
        )

    def test_multiple_landing_differnt_site(self):
        """
        Test for the new Landings referencing new site
        """

        # new site and new landing object
        site = Site(name='test', domain='test.com')
        obj = models.Landing(
            page_title = 'Another one',
            site = site
        )

        # ensure we can save successfully
        self.assertTrue(obj.save)
