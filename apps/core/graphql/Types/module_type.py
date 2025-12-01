import graphene
from graphene_django import DjangoObjectType
from ...models import Module

# ✅ IMPORTATION (Au lieu de redéfinition)
# On va chercher le fichier voisin page_type.py
from .page_type import PageType 

class ModuleType(DjangoObjectType):
    class Meta:
        model = Module
        fields = "__all__"
    
    # On déclare la liste de pages en utilisant le Type importé
    pages = graphene.List(PageType)

    def resolve_pages(self, info):
        # ✅ CORRECT : 
        # Dans ton model Page, tu as mis related_name="pages".
        # Donc Django crée l'attribut inverse '.pages' sur Module.
        # (Si tu n'avais pas mis related_name, ce serait .page_set.all())
        return self.pages.all()