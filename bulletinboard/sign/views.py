from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
from .models import BaseRegisterForm
#from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from allauth.account.views import *
#from bulletinboardapp.models import Author
from allauth.account import app_settings

class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'



# class VerificationCodeView(CreateView):

#     def usual_login_view(request):
class CodeConfirmEmailView(ConfirmEmailView):
    template_name = "account/email_confirm." + app_settings.TEMPLATE_EXTENSION
    
    def get(self, *args, **kwargs):
        if self.request.method == 'GET': 
            print('GET_SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
        if self.request.method == 'POST': 
            print('POST_SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
        try:
            self.object = self.get_object()
            if app_settings.CONFIRM_EMAIL_ON_GET:
                return self.post(*args, **kwargs)
        except Http404:
            self.object = None
        ctx = self.get_context_data()
        return self.render_to_response(ctx)

    def post(self, request, *args, **kwargs):
        if self.request.method == 'GET': 
            print('GET_SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
        if self.request.method == 'POST': 
            print('POST_SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
        self.object = confirmation = self.get_object()
        confirmation.confirm(self.request)
        if self.request.method == 'GET': 
            print('GET_SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
        if self.request.method == 'POST': 
            print('POST_SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')
        # In the event someone clicks on an email confirmation link
        # for one account while logged into another account,
        # logout of the currently logged in account.
        if (
            self.request.user.is_authenticated
            and self.request.user.pk != confirmation.email_address.user_id
        ):
            self.logout()

        get_adapter(self.request).add_message(
            self.request,
            messages.SUCCESS,
            "account/messages/email_confirmed.txt",
            {"email": confirmation.email_address.email},
        )
        if app_settings.LOGIN_ON_EMAIL_CONFIRMATION:
            resp = self.login_on_confirm(confirmation)
            if resp is not None:
                return resp
        # Don't -- allauth doesn't touch is_active so that sys admin can
        # use it to block users et al
        #
        # user = confirmation.email_address.user
        # user.is_active = True
        # user.save()
        redirect_url = self.get_redirect_url()
        if not redirect_url:
            ctx = self.get_context_data()
            return self.render_to_response(ctx)
        return redirect(redirect_url)

confirm_email = CodeConfirmEmailView.as_view()