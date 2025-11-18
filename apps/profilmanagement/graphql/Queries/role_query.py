import graphene
from ..Types.role_type import RoleType
from ...models import Role

class RoleQuery(graphene.ObjectType):
    role = graphene.Field(RoleType, id=graphene.ID(required=True))
    roles = graphene.List(RoleType)

    def resolve_role(root, info, id):
        try:
            return Role.objects.get(pk=id)
        except Role.DoesNotExist:
            return None

    def resolve_all_roles(root, info, **kwargs):
        return Role.objects.all()
