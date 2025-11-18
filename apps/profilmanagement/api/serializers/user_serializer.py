
from apps.core.api.serializers.BaseSerializer import BaseSerializer
from ...models import User

class UserSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = "__all__"
