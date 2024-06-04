import sys
import json
import requests
from random import choice

from django.conf import settings
from django.contrib.sites.models import Site
from PIL import Image as Img

from . import ScheduledCommand
from app.models import Schedule, Article, ArticleBot, Tag


def ask_chatgpt(token, system_text, user_text):
    """
    Fetch from chatgpt
    """

    URL = 'https://api.openai.com/v1/chat/completions'
    HEADERS = {
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/json'
    }

    data = {
        "model": "gpt-4o",
        "temperature": 0.7,
        "messages": [
            {"role": "system", "content": system_text},
            {"role": "user", "content": user_text}
        ]
    }

    # Make request
    r = requests.post(URL, headers=HEADERS, data=json.dumps(data))
    r.raise_for_status()

    # Return the message content
    return r.json()['choices'][0]['message']['content']


def ask_chatgpt_art(token, prompt):
    """
    Fetch art from chatgpt
    """

    URL = 'https://api.openai.com/v1/images/generations'
    HEADERS = {
        'Authorization': 'Bearer %s' % token,
        'Content-Type': 'application/json'
    }

    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "n": 1,
        "size": "1024x1024"
    }

    # Make request
    r = requests.post(URL, headers=HEADERS, data=json.dumps(data))
    r.raise_for_status()

    # Return the image url
    return r.json()['data'][0]['url']


class Command(ScheduledCommand):
    help = "Create article generated by ChatGPT"

    def add_arguments(self, parser):
        parser.add_argument("site_id", type=int)

    def handle(self, *args, **options):

        try:
            token = getattr(settings, 'OPENAI_API_KEY')
        except AttributeError:
            msg = 'OPENAI_API_KEY not found in settings.'
            self.log(msg, error=True)
            self.report_failure()
            sys.exit(1)

        try:
            site_id = options["site_id"]
            site = Site.objects.get(id=site_id)
        except Site.DoesNotExist:
            msg = 'Site not found.'
            self.log(msg, error=True)
            self.report_failure()
            sys.exit(1)

        articlebots = ArticleBot.objects.filter(site=site, enabled=True)
        if articlebots.count() < 1:
            msg = 'No ArticleBot found for site, or none enabled.'
            self.log(msg, error=True)
            self.report_failure()
            sys.exit(1)

        # Pick a random ArticleBot
        articlebot = choice(articlebots)
        self.log(f"Using ArticleBot '{articlebot}'")

        # wrap entire logic in try in order to log
        # to our django models
        try:

            # get random inputs from ArticleBot
            inputs = dict(
                subjects = choice(articlebot.subjects),
                actions = choice(articlebot.actions),
                things = choice(articlebot.things),
                places = choice(articlebot.places)
            )

            self.log(f"Generating content with the following inputs: f{inputs}")

            # Get or create tags for article
            _tags = [ i for i in inputs.values() ]
            tags = [ Tag.objects.get_or_create(name=i)[0] for i in _tags ]

            # format out user_text using our random inputs
            title_text = articlebot.title_text_template.format(**inputs)
            user_text = articlebot.user_text_template.format(**inputs)
            image_text = articlebot.image_template.format(**inputs)

            # ask chatgpt to generate our content
            title = ask_chatgpt(token, articlebot.system_text, f"'{title_text}'")
            # remove any markup from title
            title = title.strip('**"')
            title = title.strip('"')
            content = ask_chatgpt(token, articlebot.system_text,
                f"'{user_text}' titled '{title}', format with only html paragraphs, not metadata, and no title.")
            summary = ask_chatgpt(token, articlebot.system_text,
                f"In one or two sentences summarize: '{content}'")

            # save a new unpublished article
            article = Article(title=title, content=content, summary=summary, author=articlebot.name,
                site=site, published=False)
            article.save()

            # apply our tags to the new article
            article.tags.set(tags)

            # get artwork for article
            self.log(f"Generating image for {image_text}")
            image_url = ask_chatgpt_art(token, image_text + ", without text, artwork only.")

            # save path to media
            path = str(settings.MEDIA_ROOT) + '/uploads/' + article.slug_name + '.png'
            self.log(f"Saving image {image_url} to {path}")
            res = requests.get(image_url)

            # check if image generation was successufl
            if res.status_code == 200:
                with open(path, 'wb') as f:
                    f.write(res.content)
            else:
                msg = 'Failed to generate image for prompt.'
                self.log(msg, error=True)
                self.report_failure()
                sys.exit(1)
                raise(Exception('Failed to download image for article'))

            # convert image to jpg to compress size
            jpg_path = str(settings.MEDIA_ROOT) + '/uploads/' + article.slug_name + '.jpg'
            im = Img.open(path)
            im.save(jpg_path)

            # place the generated image on article and save with publish preferences
            article.image = '/uploads/' + article.slug_name + '.jpg'
            article.published=articlebot.auto_publish
            article.save()

            # log message to ScheduleLog is executed via schedule
            msg = f'Successfully created article "{title}" for "{site}"'
            self.log(msg)
            self.report_success()

        except Exception as e:
            self.log(e, error=True)
            self.report_failure()
            sys.exit(1)
