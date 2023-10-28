
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import ListView

from orders.models import OrderCart


class OrderCartListView(ListView):
    model = OrderCart
    template_name = 'orders/cart_list.html'
    context_object_name = 'cart_products'

    def get_queryset(self):
        return OrderCart.objects.filter(cart_item=1, user_id=self.request.user.id)


@login_required()
def add_to_cart(request, pk):
    if OrderCart.objects.filter(user_id=request.user.id,
                                product_id=pk).exists():
        quantity = OrderCart.objects.get(user_id=request.user.id,
                                product_id=pk).quantity
    else:
        quantity = 1

    # verificam daca produsul este in cosul de cumparaturi
    if OrderCart.objects.filter(user_id=request.user.id,
                                product_id=pk).exists():
        quantity += 1
        OrderCart.objects.filter(user_id=request.user.id,
                                 product_id=pk).update(quantity=quantity)
    else:
        # adauga produsul in cosul de cumparaturi
        OrderCart.objects.create(
            user_id=request.user.id,
            product_id=pk,
            cart_item=True,
            quantity=quantity,
            created_at=datetime.now()
        )

    return redirect('home')