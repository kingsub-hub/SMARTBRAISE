from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [
    path('', views.product_list, name='products'),
]
