from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import DisallowedHost

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
        'features': models.Article.on_site.filter(published=True, featured=True),
        'contact_form': contact_form
    }

    return render(request, landing.template.path, context)


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

    return render(request, landing.template.path, context)
