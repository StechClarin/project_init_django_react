from apps.core.api.controllers.BaseController import BaseController
from ..serializers import GroupSerializer
from ...services.group_service import GroupService

class GroupController(BaseController):
    serializer_class = GroupSerializer
    service_class = GroupService
