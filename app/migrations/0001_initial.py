# Generated by Django 5.0.5 on 2024-05-22 19:10

import app.models
import colorfield.fields
import django.contrib.sites.managers
import django.db.models.deletion
import django.db.models.manager
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.CreateModel(
            name="Template",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                (
                    "path",
                    models.CharField(help_text="Path to template", max_length=100),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="Contact",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("full_name", models.CharField(max_length=200)),
                ("email", models.EmailField(max_length=254)),
                ("message", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("responded", models.BooleanField(default=False)),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sites.site"
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name="Price",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("cost", models.IntegerField()),
                (
                    "checked_features",
                    models.JSONField(
                        blank=True, default=list, help_text="Features shown on card"
                    ),
                ),
                (
                    "missing_features",
                    models.JSONField(
                        blank=True,
                        default=list,
                        help_text="Missing features shown on card",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("featured", models.BooleanField(default=False)),
                ("enabled", models.BooleanField(default=True)),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sites.site"
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name="Schedule",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=200)),
                (
                    "command",
                    models.CharField(
                        choices=app.models.Schedule.get_app_commands, max_length=100
                    ),
                ),
                ("args", models.CharField(blank=True, max_length=200)),
                (
                    "interrupter",
                    models.CharField(default="/usr/local/bin/python", max_length=200),
                ),
                ("minute", models.CharField(default="*", max_length=2)),
                ("hour", models.CharField(default="*", max_length=2)),
                ("day_of_month", models.CharField(default="*", max_length=2)),
                ("month", models.CharField(default="*", max_length=2)),
                ("day_of_week", models.CharField(default="*", max_length=2)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("last_success_at", models.DateTimeField(blank=True, null=True)),
                ("last_failure_at", models.DateTimeField(blank=True, null=True)),
                ("enabled", models.BooleanField(default=True)),
            ],
            options={
                "ordering": ["-updated_at"],
                "unique_together": {("name", "command")},
            },
        ),
        migrations.CreateModel(
            name="ScheduleLog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "schedule",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="app.schedule"
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
        ),
        migrations.CreateModel(
            name="Landing",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "page_title",
                    models.CharField(
                        help_text="Sets site html title tag", max_length=100
                    ),
                ),
                (
                    "heading",
                    models.CharField(
                        help_text="Sets site heading in banner", max_length=100
                    ),
                ),
                (
                    "subheading",
                    models.CharField(
                        help_text="Sets site sub-heading in banner", max_length=100
                    ),
                ),
                (
                    "footer",
                    models.CharField(help_text="Sets site footer", max_length=100),
                ),
                (
                    "bs_navbar",
                    colorfield.fields.ColorField(
                        default="rgba(52,58,64,1)",
                        image_field=None,
                        max_length=25,
                        samples=None,
                        verbose_name="Navbar Color",
                    ),
                ),
                (
                    "bs_primary",
                    colorfield.fields.ColorField(
                        default="rgba(238, 9, 121)",
                        image_field=None,
                        max_length=25,
                        samples=None,
                        verbose_name="Primary Color",
                    ),
                ),
                (
                    "bs_secondary",
                    colorfield.fields.ColorField(
                        default="rgba(255, 106, 0)",
                        image_field=None,
                        max_length=25,
                        samples=None,
                        verbose_name="Secondary Color",
                    ),
                ),
                ("contact_enabled", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("enabled", models.BooleanField(default=True)),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sites.site"
                    ),
                ),
                (
                    "template",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.RESTRICT, to="app.template"
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name="Testimonial",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField()),
                ("author", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("enabled", models.BooleanField(default=True)),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sites.site"
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
        migrations.CreateModel(
            name="Article",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("summary", models.TextField()),
                ("content", models.TextField()),
                ("author", models.CharField(max_length=100)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("featured", models.BooleanField(default=False)),
                ("published", models.BooleanField(default=False)),
                (
                    "site",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="sites.site"
                    ),
                ),
            ],
            options={
                "ordering": ["-updated_at"],
                "unique_together": {("title", "site")},
            },
            managers=[
                ("objects", django.db.models.manager.Manager()),
                ("on_site", django.contrib.sites.managers.CurrentSiteManager()),
            ],
        ),
    ]
