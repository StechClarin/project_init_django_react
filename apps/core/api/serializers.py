# Fichier généré pour core

from rest_framework import serializers
from ..models import Module

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"


from rest_framework import serializers
from ..models import Page

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = "__all__"


from apps.core.api.serializers.BaseSerializer import BaseSerializer
from ..models import Permission

class PermissionSerializer(BaseSerializer):
    class Meta:
        model = Permission
        fields = "__all__"


from apps.core.api.serializers.BaseSerializer import BaseSerializer
from ..models import Group

class GroupSerializer(BaseSerializer):
    class Meta:
        model = Group
        fields = "__all__"

