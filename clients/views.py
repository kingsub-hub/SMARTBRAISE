from django.shortcuts import render, get_object_or_404
from .models import Client


def client_list(request):
    clients = Client.objects.all()
    return render(request, 'clients/list.html', {'clients': clients})


def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    return render(request, 'clients/detail.html', {'client': client})
