from django.urls import path
from . import views

app_name = 'commandes'

urlpatterns = [
    path('', views.order_list, name='list'),
    path('<int:pk>/', views.order_detail, name='detail'),
]
