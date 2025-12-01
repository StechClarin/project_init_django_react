from apps.core.services.BaseService import BaseService
from ..models import Car

class CarService(BaseService):
    model = Car
    
    # 1. EXPORT : Quels champs acceptes-tu d'exporter ? (Whitelist)
    # export_fields = [
    #     'username', 
    #     'email', 
    #     'first_name', 
    #     'last_name',
    #     # MAGIE : On exporte le NOM du rôle, mais on appelle la colonne 'role'
    #     {'role__name': 'role'}, 
    #     'is_active'
    # ]
    # 2. IMPORT : Quels colonnes acceptes-tu de lire ? (Whitelist)
    # (Sécurité : Si le fichier contient une colonne "id" ou "superuser", on l'ignore)
    # import_fields = [
    #     'username', 
    #     'email', 
    #     'first_name', 
    #     'last_name', 
    #     'password',
    #     # MAGIE : On lit la colonne 'role' et on cherche par 'name'
    #     {'role': {'model': Role, 'search_field': 'name'}}
    # ]
    
    export_fields = [
        'brand', 
        'model_name', 
        'year', 
        'price', 
        'is_sold'
        # Note: On n'exporte PAS 'created_at' ou 'id' si on ne veut pas
    ]

    # 2. IMPORT : Quels colonnes acceptes-tu de lire ? (Whitelist)
    # (Sécurité : Si le fichier contient une colonne "id" ou "superuser", on l'ignore)
    import_fields = [
        'brand', 
        'model_name', 
        'year', 
        'price'
    ]

    def before_validate(self, data, instance=None):
        # Le service nettoie la donnée intelligemment
        if 'immatriculation' in data:
            data['immatriculation'] = data['immatriculation'].upper().strip()
        return data