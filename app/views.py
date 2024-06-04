from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import DisallowedHost
from django.core.paginator import Paginator

from . import models
from . import forms


def index(request):
    """
    Index Page
    """

    # finding landing for the site and make sure enabled
    try:
        landing = models.Landing.on_site.get(enabled=True)
    except ObjectDoesNotExist:
        raise DisallowedHost("Not a valid site.")

    contact_form = forms.ContactForm

    if request.method == 'POST':
        contact_form = forms.ContactForm(request.POST)  # get submitted form

        # if valid save to database
        if contact_form.is_valid():
            # add site_id from request
            contact_form.cleaned_data['site'] = request.site
            # create new contact object and save
            contact = models.Contact(**contact_form.cleaned_data)
            contact.save()
            # return our thank you page
            return HttpResponseRedirect("/?thanks")

    context = {
        'landing': landing,
        'articles': models.Article.on_site.filter(published=True).order_by('-created_at')[0:3],
        'contact_form': contact_form
    }

    template = landing.template.path + '/index.html'
    return render(request, template, context)


def articles(request):
    """
    Articles Page
    """

    # finding landing for the site and make sure enabled
    try:
        landing = models.Landing.on_site.get(enabled=True)
    except ObjectDoesNotExist:
        raise DisallowedHost("Not a valid site.")

    # pagenate our articles
    articles_list = models.Article.on_site.filter(published=True)
    paginator = Paginator(articles_list, 6)  # Show 6 contacts per page.

    # get current page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'landing': landing,
        'page_obj': page_obj
    }

    template = landing.template.path + '/articles.html'
    return render(request, template, context)


def article(request, slug_name):
    """
    Article Page
    """

    # finding landing for the site and make sure enabled
    try:
        landing = models.Landing.on_site.get(enabled=True)
    except ObjectDoesNotExist:
        raise DisallowedHost("Not a valid site.")

    context = {
        'landing': landing,
        'article': models.Article.on_site.get(slug_name=slug_name, published=True)
    }

    template = landing.template.path + '/article.html'
    return render(request, template, context)
