
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView

from orders.models import OrderCart


class OrderCartListView(ListView):
    model = OrderCart
    template_name = 'orders/cart_list.html'
    context_object_name = 'cart_products'

    def get_queryset(self):
        result = (OrderCart.objects.filter(cart_item=1,
                                        user_id=self.request.user.id))
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart_products = context['cart_products']
        grand_total = sum(item.amount() for item in cart_products)
        context['grand_total'] = grand_total
        return context


class WishListView(ListView):
    model = OrderCart
    template_name = 'orders/wish_list.html'
    context_object_name = 'wish_products'

    def get_queryset(self):
        result = (OrderCart.objects.filter(wishlist_item=1,
                                        user_id=self.request.user.id))
        return result

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

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required()
def add_to_wishlist(request, pk):
    if OrderCart.objects.filter(user_id=request.user.id,
                                product_id=pk,
                                wishlist_item=True).exists():

        return redirect('wish-list')
    else:
        OrderCart.objects.create(
            user_id=request.user.id,
            product_id=pk,
            wishlist_item=True,
            quantity=1,
            created_at=datetime.now()
        )

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required()
def delete_from_cart(request, pk):
    OrderCart.objects.filter(user_id=request.user.id, id=pk).delete()

    return redirect('cart-list')

def increase_cart_quantity(request, pk):
    result = OrderCart.objects.get(id=pk)
    quantity = result.quantity
    quantity += 1
    OrderCart.objects.filter(id=pk).update(quantity=quantity)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def decrease_cart_quantity(request, pk):
    result = OrderCart.objects.get(id=pk)
    quantity = result.quantity
    if quantity == 1:
        delete_from_cart(request, pk)
    else:
        quantity -= 1
    OrderCart.objects.filter(id=pk).update(quantity=quantity)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
