from django.urls import path,re_path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView
from . import views
#from .views import upgrade_me

urlpatterns = [
     path('login/', 
          LoginView.as_view(template_name = 'flatpages/login.html'),
          name='login'),
     path('logout/', 
          LogoutView.as_view(template_name = 'flatpages/logout.html'),
          name='logout'),
     path('signup/', 
          BaseRegisterView.as_view(template_name = 'flatpages/signup.html'), 
          name='signup'),
     re_path(
        r"accounts/confirm-email/(?P<key>[-:\w]+)/$",
        views.confirm_email,
        name="account_confirm_email",
    ),
]