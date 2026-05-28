from django.contrib import admin
from .models import Order, Payment, Delivery


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'order_number',
        'client',
        'status',
        'total_amount',
        'paid_amount',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'order_number',
        'client__nom',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'amount',
        'method',
        'payment_date',
    )

    list_filter = (
        'method',
        'payment_date',
    )

    readonly_fields = (
        'payment_date',
    )


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'delivery_agent',
        'status',
        'scheduled_at',
        'delivered_at',
    )

    list_filter = (
        'status',
    )