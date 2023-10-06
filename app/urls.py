from django.urls import path
from .views import *

urlpatterns = [
    path('',index),
    path('scripe/',scripe_image,name="scripe_image"),
]