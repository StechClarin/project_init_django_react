from apps.core.api.controllers.BaseController import BaseController
from ..serializers.car_serializer import CarSerializer
from ...services.car_service import CarService

class CarController(BaseController):
    serializer_class = CarSerializer
    service_class = CarService
