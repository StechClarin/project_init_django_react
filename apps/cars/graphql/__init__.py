import graphene
from apps.cars.graphql.Queries.cars_query import CarsQuery

class Query(CarsQuery, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query)
