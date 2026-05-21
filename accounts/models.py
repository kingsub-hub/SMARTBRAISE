from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model for SMARTBRAISE.

    Fields:
    - username, email, first_name, last_name inherited from AbstractUser
    - phone: optional contact phone
    - role: simple role string (admin, manager, worker)
    """

    phone = models.CharField(max_length=30, blank=True, null=True)
    role = models.CharField(max_length=30, blank=True, default='staff')

    def __str__(self):
        return self.get_full_name() or self.username
