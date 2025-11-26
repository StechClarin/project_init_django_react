from django.db import models

class Car(models.Model):
    brand = models.CharField(max_length=100, verbose_name="Marque") # ex: Toyota
    model_name = models.CharField(max_length=100, verbose_name="Modèle") # ex: Corolla
    year = models.IntegerField(verbose_name="Année")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix")
    is_sold = models.BooleanField(default=False, verbose_name="Vendue ?")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "voiture"
        verbose_name_plural = "voitures"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.brand} {self.model_name} ({self.year})"