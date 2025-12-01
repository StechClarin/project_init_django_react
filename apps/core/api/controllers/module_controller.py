from .BaseController import BaseController
from ..serializers.module_serializer import ModuleSerializer
from ...services.module_service import ModuleService

class ModuleController(BaseController):
    serializer_class = ModuleSerializer
    service_class = ModuleService
