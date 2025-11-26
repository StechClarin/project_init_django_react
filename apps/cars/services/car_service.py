from apps.core.services.BaseService import BaseService
from ..models import Car

class CarService(BaseService):
    model = Car

    def create(self, validated_data):
        # LOGIQUE MÉTIER : On met la marque en majuscules
        if 'brand' in validated_data:
            validated_data['brand'] = validated_data['brand'].upper()
            
        # On laisse le BaseService faire l'insertion en BDD
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # TODO: Logique métier spécifique avant la mise à jour
        return super().update(instance, validated_data)

    def delete(self, instance):
        # TODO: Logique métier spécifique avant la suppression
        return super().delete(instance)
