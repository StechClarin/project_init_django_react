import graphene
from graphene_django import DjangoObjectType
from ...models import User

class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',) # Sécurité : on ne renvoie jamais le hash du mot de passe
