import graphene
from graphene_django.types import DjangoObjectType
from ...models import Cars

class CarsType(DjangoObjectType):
    class Meta:
        model = Cars
        fields = "__all__"
