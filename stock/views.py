from django.shortcuts import render
from .models import Product


def product_list(request):
    products = Product.objects.all()
    return render(request, 'stock/product_list.html', {'products': products})
from django.shortcuts import render

# Create your views here.
