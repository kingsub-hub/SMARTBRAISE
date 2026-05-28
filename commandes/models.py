from django.db import models
from django.conf import settings
from clients.models import Client


class Order(models.Model):

    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PREPARING = 'preparing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'

    STATUS_CHOICES = [
        (PENDING, 'En attente'),
        (CONFIRMED, 'Confirmée'),
        (PREPARING, 'Préparation'),
        (SHIPPED, 'En livraison'),
        (DELIVERED, 'Livrée'),
        (CANCELLED, 'Annulée'),
    ]

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name='orders'
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    order_number = models.CharField(
        max_length=50,
        unique=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    paid_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    notes = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Commande"
        verbose_name_plural = "Commandes"

    def __str__(self):
        return f"CMD-{self.order_number}"


class Payment(models.Model):

    CASH = 'cash'
    MOBILE = 'mobile'
    BANK = 'bank'

    METHOD_CHOICES = [
        (CASH, 'Espèces'),
        (MOBILE, 'Mobile Money'),
        (BANK, 'Banque'),
    ]

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    method = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        default=CASH
    )

    reference = models.CharField(
        max_length=200,
        blank=True
    )

    payment_date = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ['-payment_date']

    def __str__(self):
        return f"{self.amount} USD" 


class Delivery(models.Model):

    PENDING = 'pending'
    IN_TRANSIT = 'in_transit'
    DELIVERED = 'delivered'
    FAILED = 'failed'

    STATUS_CHOICES = [
        (PENDING, 'En attente'),
        (IN_TRANSIT, 'En cours'),
        (DELIVERED, 'Livrée'),
        (FAILED, 'Échec'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='delivery'
    )

    delivery_agent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='deliveries'
    )

    address = models.TextField()

    delivery_cost = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    scheduled_at = models.DateTimeField(
        null=True,
        blank=True
    )

    delivered_at = models.DateTimeField(
        null=True,
        blank=True
    )

    notes = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"Livraison commande {self.order.id}"