# apps/core/services/BaseService.py
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class BaseService:
    """
    Service de base contenant la logique CUD partagée.
    Nos services (ex: ProductService) hériteront de ceci.
    """
    model = None # Chaque service enfant DOIT définir son modèle

    def list(self, filters=None):
        """ Récupère une liste d'objets. """
        if filters:
            return self.model.objects.filter(**filters)
        return self.model.objects.all()

    def get_by_id(self, pk):
        """ Récupère un objet par son ID ou renvoie 404. """
        try:
            return self.model.objects.get(pk=pk)
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404(f"{self.model.__name__} non trouvé")

    def create(self, validated_data):
        """ Crée un nouvel objet. """
        return self.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """ Met à jour un objet existant. """
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance):
        """ Supprime un objet. """
        instance_id = instance.id
        instance.delete()
        return {"id": instance_id, "status": "deleted"}