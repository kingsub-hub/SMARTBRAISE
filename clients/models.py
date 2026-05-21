from django.db import models


class Client(models.Model):
    """Client: restaurants, hotels, entreprises ou particuliers."""

    COMPANY = 'company'
    INDIVIDUAL = 'individual'

    CLIENT_TYPE_CHOICES = [
        (COMPANY, 'Entreprise / Établissement'),
        (INDIVIDUAL, 'Particulier'),
    ]

    name = models.CharField(max_length=200)
    contact_name = models.CharField(max_length=200, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    address = models.TextField(blank=True)
    client_type = models.CharField(max_length=20, choices=CLIENT_TYPE_CHOICES, default=COMPANY)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name
