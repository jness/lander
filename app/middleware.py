from django.conf import settings
from django.core.exceptions import DisallowedHost
from django.contrib.sites.models import Site


class SiteMiddleware:
    """
    Determine Site based on http request
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        # remove port from domain name if set
        domain = request.get_host()
        if ':' in domain:
            domain = domain.split(':')[0]

        # lookup site by domain name
        try:
            current_site = Site.objects.get(domain=domain)
        except Site.DoesNotExist:
            raise DisallowedHost("Not a valid site.")
        
        # only allow admin on primary site
        if '/admin/' in request.path:
            if current_site.id != settings.PRIMARY_SITE:
                raise DisallowedHost("Not a valid site.")

        # only allow api on primary site
        if '/api/' in request.path:
            if current_site.id != settings.PRIMARY_SITE:
                raise DisallowedHost("Not a valid site.")

        request.current_site = current_site
        settings.SITE_ID = current_site.id

        response = self.get_response(request)
        return response

