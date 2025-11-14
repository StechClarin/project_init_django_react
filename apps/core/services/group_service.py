from apps.core.services.BaseService import BaseService
from ..models import Group

class GroupService(BaseService):
    model = Group

    def create(self, validated_data):
        # TODO: Logique métier spécifique avant la création
        # (ex: validated_data['code'] = self.generate_code())
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # TODO: Logique métier spécifique avant la mise à jour
        return super().update(instance, validated_data)

    def delete(self, instance):
        # TODO: Logique métier spécifique avant la suppression
        return super().delete(instance)
