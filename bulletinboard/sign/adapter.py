from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from .models import Confirmkey
from random import randint
from django.http import HttpResponse
from django.contrib.auth.models import User
class CustomAllauthAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        current_site = get_current_site(request)
        activate_url = self.get_email_confirmation_url(request, emailconfirmation)
        code_key_set = Confirmkey(user = emailconfirmation.email_address.user, verif_code =randint(100000, 999999))
        ctx = {
            "user": emailconfirmation.email_address.user,
            "activate_url": activate_url,
            "current_site": current_site,
            "key": emailconfirmation.key,
            "code_key": code_key_set.verif_code,
        }
        if signup:
            email_template = "account/email/email_confirmation_signup"
        else:
            email_template = "account/email/email_confirmation"
        code_key_set.save()
        self.send_mail(email_template, emailconfirmation.email_address.email, ctx)

    def confirm_email(self, request, email_address):
        verification_code = Confirmkey.objects.filter(user= User.objects.get(id = email_address.user.id))
        if request.POST.get('ver_code') != verification_code.first().verif_code:
            #print(request.path)
            return HttpResponse({"error":"This data is in database"})
        elif request.POST.get('ver_code') == verification_code.first().verif_code:
            email_address.verified = True
            email_address.set_as_primary(conditional=True)
            email_address.save()