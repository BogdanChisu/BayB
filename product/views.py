from datetime import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from product.forms import ProductForm
from product.models import Product, HistoryProduct


# Create your views here.


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                        SuccessMessageMixin, CreateView):
    model = Product
    template_name = 'product/add_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')
    success_message = (
        'Product {p_title} from manufacturer {p_manufacturer}, '
        'model {p_model} sold by - to be implemented')
    permission_required = 'product.add_product'

    def get_success_message(self, cleaned_data):
        return self.success_message.format(p_title=self.object.title,
                                           p_manufacturer=self.object.manufacturer,
                                           p_model_name=self.object.model_name)

    def form_valid(self, form):
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.title = new_product.title.title()
            new_product.manufacturer = new_product.manufacturer.upper()

            history_message = (
                f'New product {new_product.title}, '
                f'from manufacturer: {new_product.manufacturer}, '
                f'model: {new_product.model_name}, '
                f'sold by - to be implemented was created {datetime.now()}')

            HistoryProduct.objects.create(message=history_message,
                                          created_at=datetime.now(),
                                          user=self.request.user)

        return redirect('home')
