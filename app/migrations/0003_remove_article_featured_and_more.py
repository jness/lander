# Generated by Django 5.0.5 on 2024-06-04 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_articlebot_image_template'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='featured',
        ),
        migrations.RemoveField(
            model_name='articlebot',
            name='auto_feature',
        ),
    ]
