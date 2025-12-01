import graphene
from ...models import User
from ..Types.user_type import UserType

class UserQuery(graphene.ObjectType):
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    @staticmethod
    def resolve_users(root, info, **kwargs):
        # TODO: Ajouter des permissions si nécessaire (ex: seul admin peut voir)
        return User.objects.all().order_by('-date_joined')

    @staticmethod
    def resolve_user(root, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None
