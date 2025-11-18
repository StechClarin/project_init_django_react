from apps.core.api.controllers.BaseController import BaseController
from ..serializers import PermissionSerializer
from ...services.permission_service import PermissionService

class PermissionController(BaseController):
    serializer_class = PermissionSerializer
    service_class = PermissionService
