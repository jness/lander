import os

from colorfield.fields import ColorField

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.core.management import get_commands
from django.utils.text import slugify



class Template(models.Model):
    """
    Templates for rendering landing page
    """

    class Meta:
        ordering = ['-updated_at']

    name = models.CharField(max_length=100, unique=True)
    path = models.CharField(help_text="Path to template", max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Landing(models.Model):
    """
    Site specific landing page
    """

    class Meta:
        ordering = ['-updated_at']

    page_title = models.CharField(help_text="Sets site html title tag", max_length=100)
    heading = models.CharField(help_text="Sets site heading in banner", max_length=100)
    subheading = models.CharField(help_text="Sets site sub-heading in banner", max_length=100)

    link = models.URLField(blank=True, null=True)

    footer = models.CharField(help_text="Sets site footer", max_length=100)

    # site color schema
    bs_navbar = ColorField(verbose_name="Navbar Color", format="rgba", default="rgba(52,58,64,1)")
    bs_primary = ColorField(verbose_name="Primary Color", format="rgba", default="rgba(238, 9, 121)")
    bs_secondary = ColorField(verbose_name="Secondary Color", format="rgba", default="rgba(255, 106, 0)")

    # site template
    template = models.ForeignKey(Template, on_delete=models.RESTRICT)

    contact_enabled = models.BooleanField(default=True)

    # add relation to django.contrib.sites.models.Site
    # https://docs.djangoproject.com/en/5.0/ref/contrib/sites/
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.site.name
    
    def save(self, *args, **kwargs):
        if not self.pk:  # if new entry
            if Landing.objects.filter(site=self.site):  # if landing page already mapped to site
                raise ValidationError("Landing for site already exists.")
        super(Landing, self).save(*args, **kwargs)


class Tag(models.Model):
    """
    Tags for articles
    """

    class Meta:
        ordering = ['-updated_at']

    name = models.CharField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    Site specific articles
    """

    class Meta:
        ordering = ['-created_at']
        unique_together = ("title", "site")

    title = models.CharField(max_length=200)
    slug_name = models.CharField(max_length=250)
    summary = models.TextField()
    content = models.TextField()
    author = models.CharField(max_length=100)

    image = models.FileField(upload_to="uploads/", blank=True, null=True)

    # add relation to django.contrib.sites.models.Site
    # https://docs.djangoproject.com/en/5.0/ref/contrib/sites/
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    tags = models.ManyToManyField(Tag)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    featured = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    
    def save(self):
        self.slug_name = slugify(self.title)
        super().save()


class ArticleBot(models.Model):
    """
    Site specific article bot
    """

    class Meta:
        ordering = ['-created_at']
        unique_together = ("name", "site")

    name = models.CharField(help_text="Name of the ArticleBot", max_length=100)

    # fields to drive management/commands/create_ai_article
    system_text = models.CharField(help_text="The role the ai will take when generating content", max_length=255)
    title_text_template = models.CharField(help_text="The template used when asking ai to generate title", max_length=255)
    user_text_template = models.CharField(help_text="The template used when asking ai to generate content", max_length=255)
    image_template = models.CharField(help_text="The template used when asking ai to generate image", max_length=255)
    subjects = models.JSONField(help_text="List of subjects/persons to select for content generation", default=list)
    actions = models.JSONField(help_text="List of actions to select for content generation", default=list)
    things = models.JSONField(help_text="List of things to select for content generation", default=list)
    places = models.JSONField(help_text="List of places to select for content generation", default=list)

    auto_publish = models.BooleanField(default=False)
    auto_feature = models.BooleanField(default=False)

    # add relation to django.contrib.sites.models.Site
    # https://docs.djangoproject.com/en/5.0/ref/contrib/sites/
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    enabled = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Contact(models.Model):
    """
    Site specific contact
    """

    class Meta:
        ordering = ['-updated_at']

    full_name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(blank=False, null=False)
    message = models.TextField(blank=False, null=False)

    # add relation to django.contrib.sites.models.Site
    # https://docs.djangoproject.com/en/5.0/ref/contrib/sites/
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    objects = models.Manager()
    on_site = CurrentSiteManager()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    responded = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name


# make sure bulk deletes call custom delete method
# https://stackoverflow.com/questions/28896237/override-djangos-model-delete-method-for-bulk-deletion
class ScheduleQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.delete()
        super(ScheduleQuerySet, self).delete(*args, **kwargs)


class Schedule(models.Model):
    """
    Application wide schedules
    """

    class Meta:
        ordering = ['-updated_at']
        unique_together = ("name", "command")


    def get_app_commands():
        "List of management commands for app"
        return [ (i[0], i[0]) for i in get_commands().items() if i[1] == 'app' ]

    name = models.CharField(max_length=200, blank=False, null=False)
    command = models.CharField(max_length=100, choices=get_app_commands)
    args = models.CharField(max_length=200, blank=True)
    interrupter = models.CharField(max_length=200, default='/usr/local/bin/python')

    # store cron format as charaters to allow for wildcard (*)
    # https://www.ibm.com/docs/en/db2oc?topic=task-unix-cron-format
    minute = models.CharField(max_length=2, default='*')
    hour = models.CharField(max_length=2, default='*')
    day_of_month = models.CharField(max_length=2, default='*')
    month = models.CharField(max_length=2, default='*')
    day_of_week = models.CharField(max_length=2, default='*')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    last_success_at = models.DateTimeField(blank=True, null=True)
    last_failure_at = models.DateTimeField(blank=True, null=True)

    enabled = models.BooleanField(default=True)

    objects = ScheduleQuerySet.as_manager()  # custom query set to handle bulk delete calling delete method

    def __str__(self):
        return self.name

    def save(self):
        super().save()
        slug_name = 'django_' + slugify(self.name)

        if settings.CRON_SCHEDULES:
            if self.enabled:
                # build cron format from model fields
                schedule = f'{self.minute} {self.hour} {self.day_of_month} {self.month} {self.day_of_week}'
                
                # build full command using args if present
                command = self.command
                if self.args:
                    command = f'{self.command} {self.args}'

                # build cron job file in /etc/cron.d/
                content = f'{schedule} {settings.CRON_SCHEDULES_RUN_AS} SCHEDULE_ID={self.id} {self.interrupter} {settings.CRON_SCHEDULES_PATH}/manage.py {command}\n'

                if settings.CRON_SCHEDULES_WITH_SUDO:
                    # write file with sudo
                    os.system(f"echo '{content}' | sudo /usr/bin/tee /etc/cron.d/{slug_name}")
                else:
                    with open(f'/etc/cron.d/{slug_name}', 'w') as f:
                        f.write(content)

            else:
                if os.path.exists(f'/etc/cron.d/{slug_name}'):
                    if settings.CRON_SCHEDULES_WITH_SUDO:
                        os.system(f'sudo /usr/bin/rm -rf /etc/cron.d/{slug_name}')
                    else:
                        os.remove(f'/etc/cron.d/{slug_name}')

    def delete(self):

        if settings.CRON_SCHEDULES:
            super().delete()
            
            slug_name = 'django_' + slugify(self.name)

            if os.path.exists(f'/etc/cron.d/{slug_name}'):
                if settings.CRON_SCHEDULES_WITH_SUDO:
                    os.system(f'sudo /usr/bin/rm -rf /etc/cron.d/{slug_name}')
                else:
                    os.remove(f'/etc/cron.d/{slug_name}')


class ScheduleLog(models.Model):
    """
    Schedule logs
    """

    class Meta:
        ordering = ['-updated_at']

    content = models.TextField()
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.schedule.name
