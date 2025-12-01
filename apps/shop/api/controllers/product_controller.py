from apps.core.api.controllers.BaseController import BaseController
from ..serializers.product_serializer import ProductSerializer
from ...services.product_service import ProductService

class ProductController(BaseController):
    serializer_class = ProductSerializer
    service_class = ProductService
