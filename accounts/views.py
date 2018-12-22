import sys
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.urls import reverse
from django.shortcuts import redirect
from accounts.models import Token


def send_login_email(request):
    '''send login email'''
    email = request.POST['email']
    token = Token.objects.create(email=email)
    url = request.build_absolute_uri(
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email],
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')


def login(request):
    '''login'''
    uid = request.GET.get('token')
    user = auth.authenticate(uid=uid)
    if user is not None:
        auth.login(request, user)
    return redirect('/')
