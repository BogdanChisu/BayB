from django.http import HttpResponse
from django.views.generic import TemplateView


class PuppiesView(TemplateView):
    template_name = 'lilly_cici_sissy/puppies.html'