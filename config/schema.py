import graphene
import apps.cars.graphql

class Query(
    apps.cars.graphql.Query,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query)
