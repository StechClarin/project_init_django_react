from .BaseController import BaseController
from ..serializers.group_serializer import GroupSerializer
from ...services.group_service import GroupService

class GroupController(BaseController):
    serializer_class = GroupSerializer
    service_class = GroupService
