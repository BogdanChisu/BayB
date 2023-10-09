from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from EcommercePlatform.settings import EMAIL_HOST_USER
from userextend.forms import BusinessUserForm
from userextend.models import BusinessUser


# Create your views here.


class BusinessUserCreateView(CreateView):
    template_name = 'marketplace/create_business_user.html'
    model = BusinessUser
    form_class = BusinessUserForm
    success_url = reverse_lazy('market')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.first_name = new_user.first_name.title()
            new_user.last_name = new_user.last_name.title()
            new_user.user_name  = (f'{new_user.first_name[0].lower()}_'
                                   f'{new_user.last_name.lower().replace(" ", "")}')
            new_user.save()

            subject = "New Account Created"
            message = f"Congratulations, the username for your BayB marketplace account is: {new_user.user_name}"
            send_mail(subject, message, EMAIL_HOST_USER, [new_user.email])

            return redirect('market')