from datetime import datetime
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
            text_content = "The following content describes the details of your order"
            i = 0
            context = new_order.product_list
            html_content = get_template("orders/order_details.html").render(context)
            pprint(context)
            # html_content = ("<!DOCTYPE html>"
            #                 "<html lang='en'>"
            #                 "<head>"
            #                     "<meta name='viewport' content='width=device-width, initial-scale=1'>"
            #                     "<link href='https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css'"
            #                           "rel='stylesheet'"
            #                           "integrity='sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN'"
            #                           "crossorigin='anonymous'>"
            #                     "<link rel='stylesheet'"
            #                           "href='https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200'/>"
            #                 "</head>"
            #                 "<body>"
            #                 "<h2>Thank you for shopping at <img src='.static/images/BayB.gif'></h2>"
            #                 f"<h3>Order number {new_order.order_number}</h3>"
            #                 f"<h4>Placed by: <b>{self.request.user}</b></h4>"
            #                 f"<h4>Order time: {new_order.created_at}</h4>"
            #                 f"<table class='table'>"
            #                     f"<thead>"
            #                         f"<th>#</th>"
            #                         f"<th>Product title</th>"
            #                         f"<th>Quantity</th>"
            #                         f"<th>Price</th>"
            #                     f"</thead>"
            #                     f"<tbody>")
            # for item in new_order.product_list['data']:
            #     i += 1
            #     html_content += (f"<tr>"
            #                         f"<td>{i}</td>"
            #                         f"<td>{item['title']}</td>"
            #                         f"<td>{item['quantity']}</td>"
            #                         f"<td>{item['price']}</td>"
            #                      f"</tr>")
            # html_content += (f"<tr>"
            #                     f"<td></td"
            #                     f"<td>Grand Total</td>"
            #                     f"<td>{new_order.price}</td>"
            #                  f"</tr>"
            #                 f"</tbody>"
            #             f"</table>"
            #         "</body")


            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return redirect('home')




