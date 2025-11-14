
from apps.core.api.serializers.BaseSerializer import BaseSerializer
from ...models import Role

class RoleSerializer(BaseSerializer):
    class Meta:
        model = Role
        fields = "__all__"
