from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='catalogue'),
    path('search',views.search,name='search'),
    path('details',views.details,name='details'),
]