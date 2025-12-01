from .BaseSerializer import BaseSerializer
from ...models import Page

class PageSerializer(BaseSerializer):
    class Meta:
        model = Page
        fields = '__all__'
