import sys
import json
import requests

from django.conf import settings
from django.contrib.sites.models import Site

from . import ScheduledCommand
from app.models import Schedule, Article


def ask_chatgpt(token, search_text):
    """
    Fetch from chatgpt
    """

    URL = 'https://api.openai.com/v1/chat/completions'
    HEADERS = {
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/json'
    }

    data = {
        "model": "gpt-3.5-turbo",
        "temperature": 0.7,
        "messages": [
            {
                "role": "user",
                "content": search_text
            }
        ]
    }

    # Make request
    r = requests.post(URL, headers=HEADERS, data=json.dumps(data))
    r.raise_for_status()

    # Return the message content
    return r.json()['choices'][0]['message']['content']


class Command(ScheduledCommand):
    help = "Create article generated by ChatGPT"

    def add_arguments(self, parser):
        parser.add_argument("site_id", type=int)
        parser.add_argument("topic", type=str)

    def handle(self, *args, **options):

        try:
            token = getattr(settings, 'OPENAI_API_KEY')
        except AttributeError:
            msg = 'OPENAI_API_KEY not found in settings.'
            self.log(msg, error=True)
            self.report_failure()
            sys.exit(1)

        # wrap entire logic in try in order to log
        # to our django models
        try:
            site_id = options["site_id"]
            site = Site.objects.get(id=site_id)
            
            topic = options["topic"]

            # ask chatgpt to populate our content
            title = ask_chatgpt(token, f'Create a captivating title {topic}')
            content = ask_chatgpt(token, f'Create a blog post for "{title}" in html format')
            summary = ask_chatgpt(token, f'Summarize "{content}"')

            # save a new unpublished article
            article = Article(title=title, content=content, summary=summary, author='ChatGPT', site=site, published=False)
            article.save()

        except Exception as e:
            self.log(e, error=True)
            self.report_failure()
            sys.exit(1)

        # log message to ScheduleLog is executed via schedule
        msg = 'Successfully created article for site_id "%s"' % site_id
        self.stdout.write(self.style.SUCCESS(msg))
        self.log(msg)
        self.report_success()
