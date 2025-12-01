from .BaseController import BaseController
from ..serializers.permission_serializer import PermissionSerializer
from ...services.permission_service import PermissionService

class PermissionController(BaseController):
    serializer_class = PermissionSerializer
    service_class = PermissionService
