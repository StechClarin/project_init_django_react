import graphene
from graphene_django.types import DjangoObjectType
from ...models import Role

class RoleType(DjangoObjectType):
    class Meta:
        model = Role
        fields = "__all__"
