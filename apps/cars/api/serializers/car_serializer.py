
from apps.core.api.serializers.BaseSerializer import BaseSerializer
from ...models import Car

class CarSerializer(BaseSerializer):
    class Meta:
        model = Car
        fields = "__all__"
