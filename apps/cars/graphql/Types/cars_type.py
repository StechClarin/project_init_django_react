import graphene
from graphene_django.types import DjangoObjectType
from ...models import Car

class CarType(DjangoObjectType):
    class Meta:
        model = Car
        fields = "__all__"
        
    # Champ calculé pour l'affichage (Bonus)
    display_name = graphene.String()
    
    def resolve_display_name(self, info):
        return f"{self.brand} - {self.model_name}"