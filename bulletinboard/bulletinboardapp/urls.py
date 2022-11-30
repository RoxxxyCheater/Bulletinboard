from django.urls import path
from .views import Author,AdDetail,Ads,Comment,AdAdd,AdDeleteView,AdUpdateView
from . import views
from protect.views import upgrade_me

urlpatterns = [
    path('', Ads.as_view()),
    path('<int:pk>', AdDetail.as_view(), name='ad'),
    path('authors/', Author.as_view()),
    path('comments/', Comment.as_view()),
    path('add_ad/', AdAdd.as_view(), name='add_create'),
    path('ad_delete/<int:pk>/', AdDeleteView.as_view(), name='ad_delete'),
    path('ad_update/<int:pk>/', AdUpdateView.as_view(), name='ad_update'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
]