import graphene
from apps.cars.graphql.Types.cars_type import CarsType
from apps.cars.models.car import Car

class CarsQuery(graphene.ObjectType):
    car = graphene.Field(CarsType, id=graphene.ID(required=True))
    cars = graphene.List(CarsType)

    def resolve_car(root, info, id):
        try:
            return Car.objects.get(pk=id)
        except Car.DoesNotExist:
            return None

    def resolve_cars(root, info, **kwargs):
        return Car.objects.all()
