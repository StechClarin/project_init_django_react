import graphene
from graphene_django import DjangoObjectType
from ...models import Page

class PageType(DjangoObjectType):
    class Meta:
        model = Page
        fields = "__all__"
        # Note : Graphene convertit automatiquement JSONField (permission_tags) 
        # en GenericScalar ou JSONString. C'est géré.