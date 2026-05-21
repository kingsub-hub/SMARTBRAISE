from django.contrib import admin
from .models import Batch


@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'produced_at', 'quantity')
    readonly_fields = ('produced_at',)
