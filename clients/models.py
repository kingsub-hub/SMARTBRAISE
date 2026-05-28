from django.db import models


class Client(models.Model):
    """Clients de SMARTBRAISE RDC"""

    COMPANY = 'company'
    INDIVIDUAL = 'individual'

    CLIENT_TYPE_CHOICES = [
        (COMPANY, 'Entreprise / Établissement'),
        (INDIVIDUAL, 'Particulier'),
    ]

    name = models.CharField(
        max_length=200,
        verbose_name="Nom du client"
    )

    contact_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Personne de contact"
    )

    email = models.EmailField(
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name="Ville"
    )

    commune = models.CharField(
        max_length=100,
        blank=True
    )

    client_type = models.CharField(
        max_length=20,
        choices=CLIENT_TYPE_CHOICES,
        default=INDIVIDUAL
    )

    active = models.BooleanField(
        default=True
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
        verbose_name = "Client"
        verbose_name_plural = "Clients"

    def __str__(self):
        return self.name