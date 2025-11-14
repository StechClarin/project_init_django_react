from apps.core.api.controllers.BaseController import BaseController
from ..serializers import UserSerializer
from ...services.user_service import UserService

class UserController(BaseController):
    serializer_class = UserSerializer
    service_class = UserService
