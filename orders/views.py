import os
from datetime import datetime

from pprint import pprint

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect, request
from django.shortcuts import  redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView


from orders.forms import PlaceOrderForm
from orders.models import OrderCart, PlaceOrder
from orders.utils import generate_order_pdf

from django.core.mail import EmailMultiAlternatives


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
    if OrderCart.objects.filter(user_id=request.user.id, id=pk,
                                wishlist_item=1).exists():
        OrderCart.objects.filter(user_id=request.user.id, id=pk).update(
            cart_item=0)
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
    OrderCart.objects.filter(user_id=request.user.id, id=pk).update(
        cart_item=1, wishlist_item=0)
    return redirect('cart-list')

class PlaceOrderCreateView(LoginRequiredMixin, CreateView):
    template_name = 'orders/place_order.html'
    model = PlaceOrder
    form_class = PlaceOrderForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.is_valid():
            new_order = form.save(commit=False)

            # user_id
            new_order.user_id = self.request.user.id

            # order number
            generic_order = PlaceOrder.objects.count()
            new_order.order_number = f'Bay-B{generic_order}'

            # product list
            products = {'data': []}
            final_price = 0
            products_per_user = OrderCart.objects.filter(
                user_id=self.request.user.id, cart_item=1)

            for item in products_per_user:
                products['data'].append({'title': item.product.title,
                                         'price': f'{item.product.price}',
                                         'quantity': item.quantity,
                                         'amount': f'{item.product.price * item.quantity}'
                                         })
                final_price += item.product.price * item.quantity

            new_order.product_list = products
            pprint(products)

            # price
            new_order.price = final_price

            # invoice_address
            new_order.invoice_address = new_order.delivery_address

            # created_at
            new_order.created_at = datetime.now()
            new_order.save()

            # Generate pd and save it to the order
            pdf_content = generate_order_pdf(new_order)
            new_order.pdf_file.save(f"{new_order.order_number}_invoice.pdf",
                                    ContentFile(pdf_content.read()))

            # delete items from order_cart
            for item in products_per_user:
                OrderCart.objects.filter(id=item.id).delete()



            # send order details by email
            subject = f"Thank you for shopping at BayB!"
            from_email = "office@bogdan-chisu.ro"
            to = f"{self.request.user.email}"
            text_content = None
            html_content = ("<h3><p>Thank you for your order,</p></h3>"
                            "<br>"
                            "<p>Please find enclosed in the attachment "
                            "the details of your order""</p>"
                            "<p>Warmest regards,</p>"
                            "<p>Your <b style='color: red;'>Bay-B</b> team!</p>")


            email = EmailMultiAlternatives(subject, text_content, from_email, [to])

            # Attach the PDF file
            pdf_file_name = f'Bay-B{new_order.id}_invoice.pdf'
            print(f'The order file is: {pdf_file_name}')
            email.attach(pdf_file_name, new_order.pdf_file.read(),
                         'application/pdf')
            email.content_subtype = 'pdf'
            email.attach_alternative(html_content, "text/html")

            email.send()

            return redirect('home')
