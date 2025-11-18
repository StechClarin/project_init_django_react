# apps/core/api/serializers/BaseSerializer.py
from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    """
    Serializer de base.
    Tous nos serializers de modèle en hériteront.
    """
    class Meta:
        abstract = True