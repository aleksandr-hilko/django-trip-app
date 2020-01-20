from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.core.cache import cache
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.utils import geolocator

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        template_name = "index.html"
        return template_name


@api_view(["GET"])
def geocode_addr(request):
    """ Geocode incoming address.

        :returns: List of possible location addresses """
    addr = request.query_params.get("query")
    addr_coord_dict = {}

    if addr in cache:
        print("from cache")
        addr_coord_dict = cache.get(addr)
    else:
        geo_locations = geolocator.geocode(addr, exactly_one=False)
        if geo_locations:
            addr_coord_dict = {
                loc.address: [loc.latitude, loc.longitude]
                for loc in geo_locations[:5]
            }
        cache.set(addr, addr_coord_dict, timeout=CACHE_TTL)

    return Response(addr_coord_dict)
