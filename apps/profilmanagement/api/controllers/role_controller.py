from apps.core.api.controllers.BaseController import BaseController
from ..serializers import RoleSerializer
from ...services.role_service import RoleService

class RoleController(BaseController):
    serializer_class = RoleSerializer
    service_class = RoleService
