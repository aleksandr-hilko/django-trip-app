from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.utils import geolocator


class IndexTemplateView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        template_name = "index.html"
        return template_name


@api_view(["GET"])
def geocode_addr(request):
    """ Geocode incoming address.

        :returns: List of possible location addresses """
    addr = request.query_params.get("query")
    geo_locations = geolocator.geocode(addr, exactly_one=False)
    addr_coord_dict = {}
    if geo_locations:
        addr_coord_dict = {
            loc.address: [loc.latitude, loc.longitude]
            for loc in geo_locations[:5]
        }
    return Response(addr_coord_dict)
