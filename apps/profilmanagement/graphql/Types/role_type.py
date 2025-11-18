import graphene
from graphene_django.types import DjangoObjectType
from ...models import Role

class RoleType(DjangoObjectType):
    class Meta:
        model = Role
        fields = "__all__"
        def resolve_user_count(self, info):
            return self.user_set.count()