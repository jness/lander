# Generated by Django 5.0.5 on 2024-06-05 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_article_thumbnail'),
    ]

    operations = [
        migrations.AddField(
            model_name='landing',
            name='about',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='landing',
            name='disclaimer',
            field=models.TextField(blank=True, null=True),
        ),
    ]