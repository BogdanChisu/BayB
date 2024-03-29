from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, \
    PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, \
    DetailView

from category.models import Category, HistoryCategory
from category.forms import CategoryForm, CategoryUpdateForm


class CategoryCreateView(LoginRequiredMixin, PermissionRequiredMixin,
                         SuccessMessageMixin, CreateView):
    template_name = 'category/add_category.html'
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy('home')
    success_message = ('Category {category_name} was added succesfully')
    permission_required = 'category.add_category'

    def get_success_message(self, cleaned_data):
        return self.success_message.format(pname=self.object.name)

    def form_valid(self, form):
        if form.is_valid():
            new_category = form.save(commit=False)

            new_category.name = new_category.name.title()
            new_category.save()

            history_message = (f'Category {new_category.name}'
                               f' was created {datetime.now()}')
            HistoryCategory.objects.create(message=history_message,
                                          created_at=datetime.now(),
                                          user=self.request.user)

        return redirect('home')


class CategoryListView(ListView):
    template_name = 'category/list_of_categories.html'
    model = Category
    context_object_name = 'all_categories'

    def get_queryset(self):
        return Category.objects.all()

class CategoryUpdateView(LoginRequiredMixin, PermissionRequiredMixin,
                         UpdateView):
    template_name = 'category/update_category.html'
    model = Category
    form_class = CategoryUpdateForm
    success_url = reverse_lazy('list-of-categories')
    permission_required = 'category.change_category'

class CategoryDeleteView(LoginRequiredMixin, PermissionRequiredMixin,
                         DeleteView):
    template_name = 'category/delete_view.html'
    model = Category
    success_url = reverse_lazy('list-of-categories')
    permission_required = 'category.delete_category'


class CategoryDetailView(LoginRequiredMixin, PermissionRequiredMixin,
                         DetailView):
    template_name = 'category/detail_category.html'
    model = Category
    permission_required = 'category/view_category'