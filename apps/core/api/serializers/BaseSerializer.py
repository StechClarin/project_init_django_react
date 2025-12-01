# apps/core/api/serializers/BaseSerializer.py
from rest_framework import serializers

class SmartRelatedField(serializers.PrimaryKeyRelatedField):
    """
    Un champ hybride magique pour les relations (ForeignKey / ManyToMany).
    - ENTRÉE (Write) : Accepte des IDs (ex: [1, 2]).
    - SORTIE (Read)  : Renvoie la représentation string (ex: ["Admin", "Manager"]).
    """
    def __init__(self, **kwargs):
        # Par défaut, on veut lire l'ID en entrée
        super().__init__(**kwargs)

    def use_pk_only_optimization(self):
        return False

    def to_representation(self, value):
        # C'est ici la magie : au lieu de renvoyer l'ID, on renvoie le __str__ de l'objet
        return str(value)
class BaseSerializer(serializers.ModelSerializer):
    """
    Serializer de base.
    Tous nos serializers de modèle en hériteront.
    """
    class Meta:
        abstract = True