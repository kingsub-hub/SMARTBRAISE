from django.shortcuts import render
from .models import Batch


def batch_list(request):
    batches = Batch.objects.all()
    return render(request, 'production/list.html', {'batches': batches})
