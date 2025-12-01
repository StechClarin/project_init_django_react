from apps.core.services.BaseService import BaseService
from ..models import Role

class RoleService(BaseService):
    model = Role

    # Les méthodes create, update, delete sont gérées par BaseService
    pass
