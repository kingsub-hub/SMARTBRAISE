from django.db import models


class Batch(models.Model):
    """Production batch: lot de production de braises."""

    name = models.CharField(max_length=200)
    produced_at = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField()
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} ({self.quantity})"
