import graphene
from .Queries.module_query import ModuleQuery

class Query(ModuleQuery, graphene.ObjectType):
    pass
