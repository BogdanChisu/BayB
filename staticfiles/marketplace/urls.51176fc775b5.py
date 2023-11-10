from django.urls import path

from marketplace.views import MarketplaceTemplateView

urlpatterns = [
    path("marketplace/", MarketplaceTemplateView.as_view(), name="market"),
]