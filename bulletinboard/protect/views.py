from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from ignore import DEFAULT_FROM_EMAIL
class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'flatpages/default.html'


# @login_required
# def upgrade_me(self):
#     print('!!!! SUCCESS !!!!')

#     for user in User.objects.all():
#         users_i_email = self.user.email
#         if users_i_email != user.email:
#             msg = EmailMultiAlternatives(
#                 subject= self.POST.get('title_email'),
#                 body=self.POST.get('content_email'),
#                 from_email= DEFAULT_FROM_EMAIL,
#                 to=[user.email],
#             )
#             msg.send()
#     return HttpResponse(f"<h2>Email sending was successful!</h2>Press <a href='http://127.0.0.1:8000/callboard/'>here</a> to main page")


@login_required
def upgrade_me(self):
    recipient = User.objects.all() if not self.POST.get('personal_email').strip() else User.objects.filter(email=self.POST.get('personal_email'))
    if not recipient:
        return HttpResponse(f"<h2>Invalid email - the user with the entered email is not in the database.</h2> <h4>Press <a href='http://127.0.0.1:8000/callboard/'>here</a> to main page</h4>")
    for user in recipient:
        #users_i_email = 
        if self.user.email != user.email:
            msg = EmailMultiAlternatives(
                subject= self.POST.get('title_email'),
                body=self.POST.get('content_email'),
                from_email= DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.send()
    return HttpResponse(f"<h2>Email sending was successful!</h2>Press <a href='http://127.0.0.1:8000/callboard/'>here</a> to main page")
    