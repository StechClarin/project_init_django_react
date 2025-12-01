import graphene
from apps.cars.graphql.Types.cars_type import CarType
from apps.cars.models.car import Car

class CarsQuery(graphene.ObjectType):
    car = graphene.Field(CarType, id=graphene.ID(required=True))
    cars = graphene.List(CarType)

    # Champ 'car' (Singulier) -> Retourne CarType
    car = graphene.Field(CarType, id=graphene.ID(required=True))
    
    # Champ 'cars' (Pluriel) -> Retourne une Liste de CarType
    cars = graphene.List(
        CarType, 
        is_sold=graphene.Boolean(),
        brand=graphene.String()
    )

    def resolve_car(root, info, id):
        try:
            return Car.objects.get(pk=id)
        except Car.DoesNotExist:
            return None

    def resolve_cars(root, info, is_sold=None, brand=None, **kwargs):
        qs = Car.objects.all()
        if is_sold is not None:
            qs = qs.filter(is_sold=is_sold)
        if brand:
            qs = qs.filter(brand__icontains=brand)
        return qs