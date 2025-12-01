from .BaseSerializer import BaseSerializer
from ...models import Group

class GroupSerializer(BaseSerializer):
    class Meta:
        model = Group
        fields = '__all__'
