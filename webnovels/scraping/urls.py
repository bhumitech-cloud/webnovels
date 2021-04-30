from django.urls import path
from . import views

urlpatterns = [
    path('login',views.login,name='login'),
    path('scrap',views.scrap,name='scrap'),
    path('insertNovel',views.insertNovel,name='insertNovel'),
]