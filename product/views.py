from datetime import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin, \
    LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DetailView

from product.forms import ProductForm, ProductUpdateForm
from product.models import Product, HistoryProduct


# Create your views here.


class ProductCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                        SuccessMessageMixin, CreateView):
    model = Product
    template_name = 'product/add_product.html'
    form_class = ProductForm
    success_url = reverse_lazy('home')
    success_message = ('Product: {p_category}, {p_model_name} was added'
                       'successfully!')
    permission_required = 'product.add_product'

    def get_success_message(self, cleaned_data):
        return self.success_message.format(p_category=self.object.category,
                                           p_model_name=self.object.model_name)

    def form_valid(self, form):
        if form.is_valid():
            new_product = form.save(commit=False)
            new_product.model_name = new_product.model_name.title()
            new_product.save()

            history_message = (f'New product {new_product.model_name},'
                               f' from category {new_product.category.name},'
                               f' was created {datetime.now()}')
            HistoryProduct.objects.create(message=history_message,
                                          created_at=datetime.now(),
                                          user=self.request.user)

        return redirect('list-of-products')

class ProductListView(ListView):
    model = Product
    template_name = 'product/list_of_products.html'
    context_object_name = 'all_products'

    def get_queryset(self):
        return Product.objects.filter(is_active=True)


class ProductUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                        UpdateView):
    template_name = 'product/update_product.html'
    model = Product
    form_class = ProductUpdateForm
    success_url = reverse_lazy('list-of-products')
    permission_required = 'product.change_product'


class ProductDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                        DetailView):
    template_name = 'product/product_detail.html'
    model = Product
    permission_required = 'product.view_product'


@login_required
@permission_required('product.delete_product')
def delete_product_modal(request, pk):
    Product.objects.filter(id=pk).delete()
    return redirect('list-of-products')

