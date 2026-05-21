from django.db import models


class Product(models.Model):
	"""Produit stocké: type de braise ou consommable lié."""

	name = models.CharField(max_length=200)
	sku = models.CharField(max_length=100, blank=True)
	description = models.TextField(blank=True)
	unit = models.CharField(max_length=50, default='kg')
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.name


class StockMovement(models.Model):
	IN = 'in'
	OUT = 'out'

	DIRECTION_CHOICES = [
		(IN, 'Entrée'),
		(OUT, 'Sortie'),
	]

	product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
	direction = models.CharField(max_length=10, choices=DIRECTION_CHOICES)
	quantity = models.DecimalField(max_digits=10, decimal_places=2)
	reason = models.CharField(max_length=200, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ['-created_at']

	def __str__(self):
		return f"{self.get_direction_display()} {self.quantity} {self.product}"

