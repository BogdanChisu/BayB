import os
from datetime import datetime
from email.mime import image
from email.mime.image import MIMEImage
from pprint import pprint
from random import randint
from urllib import request

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.db.models import Sum
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template import Context
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from orders.forms import PlaceOrderForm
from orders.models import OrderCart, PlaceOrder


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
                                product_id=pk, cart_item=1).exists():
        quantity = OrderCart.objects.get(user_id=request.user.id,
                                product_id=pk).quantity
    else:
        quantity = 1

    # verificam daca produsul este in cosul de cumparaturi
    if OrderCart.objects.filter(user_id=request.user.id,
                                product_id=pk, cart_item=1).exists():
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
    if OrderCart.objects.filter(user_id=request.user.id, id=pk, wishlist_item=1).exists():
        OrderCart.objects.filter(user_id=request.user.id, id=pk).update(cart_item=0)
        return redirect('cart-list')
    else:
        OrderCart.objects.filter(user_id=request.user.id, id=pk).delete()
        return redirect('cart-list')

@login_required()
def delete_from_wishlist(request, pk):
    if OrderCart.objects.filter(user_id=request.user.id, id=pk,
                                cart_item=1).exists():
        OrderCart.objects.filter(user_id=request.user.id, id=pk).update(
            wishlist_item=0)
        return redirect('wish-list')
    else:
        OrderCart.objects.filter(user_id=request.user.id, id=pk).delete()
        return redirect('wish-list')

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

@login_required()
def move_favorites_to_cart(request, pk):
    OrderCart.objects.filter(user_id=request.user.id, id=pk).update(cart_item=1, wishlist_item=0)
    return redirect('cart-list')


class PlaceOrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'orders/place_order.html'
    model = PlaceOrder
    form_class = PlaceOrderForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.is_valid():
            new_order = form.save(commit=False)

            #user_id
            new_order.user_id = self.request.user.id

            # order number
            generic_order = randint(1, 100)
            new_order.order_number = f'ESHOP_{generic_order}'


            # product list
            products = {'data': []}
            final_price = 0
            products_per_user = OrderCart.objects.filter(user_id=self.request.user.id, cart_item=1)

            for item in products_per_user:
                products['data'].append({'title': item.product.title,
                                         'quantity': item.quantity,
                                         'price': f'{item.product.price * item.quantity}'
                                         })
                final_price += item.product.price * item.quantity
                OrderCart.objects.filter(id=item.id).delete()
            new_order.product_list = products
            pprint(products)

            # price
            new_order.price = final_price

            # invoice_address
            new_order.invoice_address = new_order.delivery_address

            # created_at
            new_order.created_at = datetime.now()
            new_order.save()

            # send order details by email
            subject = f"Thank you {self.request.user} for shopping at BayB!"
            from_email = "office@bogdan-chisu.ro"
            to = f"{self.request.user.email}"
            context = new_order.product_list
            context['data'].append({'title': '',
                                    'quantity': 'Grand Total',
                                    'price': new_order.price})
            html_content = get_template("orders/order_details.html").render(context)
            pprint(context)
            msg = EmailMultiAlternatives(
                subject,
                html_content,
                from_email,
                [to]
            )
            image_path = 'static/images/BayB.gif'
            msg.attach_file(image_path)
            msg.content_subtype = 'html'


            msg.send()

            return redirect('home')




