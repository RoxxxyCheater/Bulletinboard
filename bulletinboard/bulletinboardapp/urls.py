from django.urls import path
from .views import Author,Ad,Ads,Comment,AdAdd
from . import views

urlpatterns = [
    path('', Ads.as_view()),
    #path('<int:pk>', Ad.as_view(), name='post'),
    path('authors/', Author.as_view()),
    path('comments/', Comment.as_view()),
    path('add_ad/', AdAdd.as_view(), name='post_create'),
]