from base64 import urlsafe_b64encode
import email
from email.message import EmailMessage
import imp
from lib2to3.pgen2.tokenize import generate_tokens
import re
from turtle import end_fill
import django
from django.conf import settings
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from Authentication_Module import settings
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
import AuthenticationModule
import tkinter

# Create your views here.

def home(request):
    return render(request, "AuthenticationModule/index.html")

def register(request):

    if request.method == "POST":
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        password=request.POST['password']
        cnfpassword=request.POST['cnfpassword']

        if User.objects.filter(username=username):
            messages.error(request, "Username is already registered, kindly try some other usernames")
            return redirect('/register')

        if User.objects.filter(email=email):
            messages.error(request, "Email is already registered, kindly try some other emails")
            return redirect('/register')

        if len(username)>10:
            messages.error(request, "Username must be of upto chars")
            return redirect('/register')

        SpecialSym =['$', '@', '#', '%']
        val = True

        if len(password)<8:
            messages.error(request, "Password should have minimum 8 chaarcters")
            return redirect('/register')

        if len(password)>20:
            messages.error(request, "Password should have maximum 20 chaarcters")
            return redirect('/register')

        if not any(char.isdigit() for char in password):
            messages.error(request, "Password should have at least one numeral")
            return redirect('/register')
          
        if not any(char.isupper() for char in password):
            messages.error(request, "Password should have atleast an uppercase letter")
            return redirect('/register')   
          
        if not any(char.islower() for char in password):
            messages.error(request, "Password should have  a lowercase letter")
            return redirect('/register')
          
        if not any(char in SpecialSym for char in password):
            messages.error(request, "Password should have maximum 20 chaarcters")
            return redirect('/register')

        if password!=cnfpassword:
            messages.error(request, "Password didn't match")
            return redirect('/register')
        

        myuser=User.objects.create_user(username, email, password)
        myuser.first_name=fname
        myuser.last_name=lname
        myuser.email=email
        myuser.username=username
        myuser.is_active= False
        myuser.save()

        messages.success(request, "You have been registered successfully, Please confirm your email by clicking on the link sent to your registered email id in order to activate your account")


        #Welcom Email
        
        subject= "Welcome to AuthenticationModule App!"
        message = "Hello "+myuser.first_name+ "!! \n"+"Welcome to AuthenticationModule App! \nThank you for visiting our website \nPlease confirm your email before logging in \n \nThanks & Regards \nRahmatullah"
        from_email=settings.EMAIL_HOST_USER
        to_list=[myuser.email]
        send_mail(subject, message, 'Rahmatullah Sayed<dev.rahmat.authm@gmail.com>', to_list, fail_silently=True)

        #Email Address Confirmation

        current_site = get_current_site(request)
        email_subject ="Confirm your email @ AuthenticationModule App! "
        message2 = render_to_string('emailconf.html',{
            'name': myuser.first_name,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser),
        })
        email = EmailMessage(
            email_subject,
            message2,
            'Rahmatullah Sayed<dev.rahmat.authm@gmail.com>',
            [myuser.email],
        )
        email.fail_silently=True
        email.send()

        return redirect('/login')

    return render (request, "AuthenticationModule/register.html")

def loginn(request):

    if request.method == "POST":
        username=request.POST['username']
        password=request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            username=user.username
            fname=user.first_name
            lname=user.last_name
            email=user.email
            return render(request, "AuthenticationModule/loggedin.html", {'fname': fname, 'lname': lname, 'email': email, 'username': username})

        else:
            messages.error(request, "Bad credentials, Please try with correct one. ")
            return redirect('/login')

    return render (request, "AuthenticationModule/login.html")

def logoutt(request):
    logout(request)
    messages.success(request, "You've been logged out successfully")
    return redirect('home')

def loggedin(request):
    return render(request, "AuthenticationModule/loggedin.html")


def resetpass(request):
    return render(request, "AuthenticationModule/resetpass.html")

def activate(request, uidb64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        myuser=User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser=None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active=True
        myuser.save()
        login(request, myuser)
        messages.success(request, "Your account has now been activated, you may login to our app now.")
        return redirect ('home')
    else:
        return render(request, 'activefail.html')