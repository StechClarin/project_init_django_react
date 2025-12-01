from .BaseSerializer import BaseSerializer
from ...models import Module

class ModuleSerializer(BaseSerializer):
    class Meta:
        model = Module
        fields = '__all__'
