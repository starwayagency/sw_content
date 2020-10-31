from django.urls import path, include 

from .views import * 


urlpatterns = [
    path('contents/', contents_list),
    path('contents/<code>/', content),
]
