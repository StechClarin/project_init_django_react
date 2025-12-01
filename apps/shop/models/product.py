from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "product"
        verbose_name_plural = "products"
        ordering = ['-created_at']

    def __str__(self):
        return self.name or f"Product #{self.pk}"
