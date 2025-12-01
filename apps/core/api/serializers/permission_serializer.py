from .BaseSerializer import BaseSerializer
from ...models import Permission

class PermissionSerializer(BaseSerializer):
    class Meta:
        model = Permission
        fields = '__all__'
