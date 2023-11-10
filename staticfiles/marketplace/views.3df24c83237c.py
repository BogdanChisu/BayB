from django.http import request
from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.


class MarketplaceTemplateView(TemplateView):
    template_name = 'marketplace/marketplace.html'
