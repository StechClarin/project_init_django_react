from .BaseController import BaseController
from ..serializers.page_serializer import PageSerializer
from ...services.page_service import PageService

class PageController(BaseController):
    serializer_class = PageSerializer
    service_class = PageService
