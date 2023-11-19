from datetime import datetime

from django.contrib.auth.models import User, Group
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from EcommercePlatform.settings import EMAIL_HOST_USER
from userextend.forms import UserForm, UserBusinessForm
from userextend.models import History, CustomUser


# Create your views here.


def check_username(usr_name):
    all_users = CustomUser.objects.filter(username=usr_name)
    user_name_initial = usr_name
    user_count = 0
    while len(all_users) > 0:
        usr_name = user_name_initial + '_' + str(user_count)
        all_users = User.objects.filter(username=usr_name)
        user_count += 1
    return usr_name


class UserCreateView(CreateView):
    template_name = 'userextends/create_user.html'
    model = CustomUser
    form_class = UserForm
    success_url = reverse_lazy('home')


    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.first_name = new_user.first_name.title()
            new_user.last_name = new_user.last_name.title()

            generate_username = f'{new_user.first_name[0].lower()}_{new_user.last_name.lower().replace(" ", "")}'
            if CustomUser.objects.filter(username=generate_username).exists:
                new_user.username = check_username(generate_username)
            else:
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

class UserBusinessCreateview(CreateView):
    template_name = 'userextends/create_business_user.html'
    model = CustomUser
    form_class = UserBusinessForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.first_name = new_user.first_name.title()
            new_user.last_name = new_user.last_name.title()
            new_user.company_name = new_user.company_name.title()
            get_group = Group.objects.get(name='Business')


            generate_username = f'{new_user.first_name[0].lower()}_{new_user.last_name.lower().replace(" ", "")}'
            if CustomUser.objects.filter(username=generate_username).exists:
                new_user.username = check_username(generate_username)
            else:
                new_user.username = (f'{new_user.first_name[0].lower()}_{new_user.last_name.lower().replace(" ", "")}')

            new_user.save()
            new_user.groups.add(get_group)

            # send mail user creation
            subject = "New Account Created"
            message = f"Congratulations, the username for your BayB marketplace account is: {new_user.username}"
            send_mail(subject, message, EMAIL_HOST_USER, [new_user.email])

            # history
            history_text = f'{new_user.first_name} {new_user.last_name} was successfully created on {datetime.now()}'
            History.objects.create(text = history_text, created_at=datetime.now())

            return redirect('login')