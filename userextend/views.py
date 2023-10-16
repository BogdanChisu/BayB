from datetime import datetime

from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from EcommercePlatform.settings import EMAIL_HOST_USER
from userextend.forms import UserForm
from userextend.models import History


# Create your views here.


class UserCreateView(CreateView):
    template_name = 'userextends/create_user.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('market')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.first_name = new_user.first_name.title()
            new_user.last_name = new_user.last_name.title()
            new_user.username = (f'{new_user.first_name[0].lower()}_{new_user.last_name.lower().replace(" ", "")}')
            new_user.save()

            # send mail user creation
            subject = "New Account Created"
            message = f"Congratulations, the username for your BayB marketplace account is: {new_user.username}"
            send_mail(subject, message, EMAIL_HOST_USER, [new_user.email])

            # history
            history_text = f'{new_user.first_name} {new_user.last_name} was successfully created on {datetime.now()}'
            History.objects.create(text = history_text, created_at=datetime.now())

            return redirect('login')