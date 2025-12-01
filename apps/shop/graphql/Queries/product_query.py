import graphene
from ..Types.product_type import ProductType
from ...models import Product

class ProductQuery(graphene.ObjectType):
    product = graphene.Field(ProductType, id=graphene.ID(required=True))
    products = graphene.List(ProductType)

    def resolve_product(root, info, id):
        try:
            return Product.objects.get(pk=id)
        except Product.DoesNotExist:
            return None

    def resolve_products(root, info, **kwargs):
        return Product.objects.all()
