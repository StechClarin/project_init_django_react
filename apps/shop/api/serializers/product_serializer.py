from apps.core.api.serializers.BaseSerializer import BaseSerializer
from ...models import Product

class ProductSerializer(BaseSerializer):
    class Meta:
        model = Product
        fields = "__all__"
