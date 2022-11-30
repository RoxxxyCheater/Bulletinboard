from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/default.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_staff'] = self.request.user.is_superuser
        return context

    def post(self, *args, **kwargs):
        print(self, *args, **kwargs)
        print('!!!! BIG SUCCESS !!!!')
        user = self.request.user
        print(user, self.request.user.username)
        return upgrade_me(self, user, *args, **kwargs)

@login_required

def upgrade_me(self):
    print('!!!! SUCCESS !!!!')
    for user in User.objects.all():
        users_i_email = self.user.email#user.objects.filter('email').values()
        if users_i_email != user.email:
            # users = users_i_email.get('newsletters_form_request')
            #print(user, users)
            msg = EmailMultiAlternatives(

            )
    return HttpResponse(f"<h2>Name: {user},{users}")