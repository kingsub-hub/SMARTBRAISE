from django.shortcuts import render, get_object_or_404
from .models import Order


def order_list(request):
    orders = Order.objects.select_related('client').all()
    return render(request, 'commandes/order_list.html', {'orders': orders})


def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'commandes/order_detail.html', {'order': order})
