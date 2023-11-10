from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from rating.forms import RatingForm
from rating.models import Rating


class RatingCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                       CreateView):
    template_name = 'rating/create_rating.html'
    model = Rating
    form_class = RatingForm
    success_url = reverse_lazy('home') # list of product ratings
    permission_required = 'rating.add_rating'
