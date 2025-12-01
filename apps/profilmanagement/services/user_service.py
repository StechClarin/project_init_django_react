from apps.core.services.BaseService import BaseService
from ..models import User, Role

class UserService(BaseService):
    model = User

    import_fields = [
        'username', 'email', 'first_name', 'last_name', 'password', 
        # On garde 'roles' comme champ texte pour l'instant, on le traite dans before_save
        'roles' 
    ]
    
    export_fields = ['username', 'email', 'roles_display', 'is_active'] # roles_display pour l'export

    def before_save(self, data, instance=None):
        """
        Gère l'assignation des rôles (Liste d'IDs ou Noms séparés par virgule).
        """
        # On extrait les rôles des données brutes pour les traiter
        # Attention : ManyToMany ne peut être sauvé qu'APRÈS la création de l'objet.
        # On stocke temporairement les rôles dans une variable d'instance du service
        self._roles_to_add = []

        raw_roles = data.pop('roles', None) # On retire 'roles' pour ne pas planter le create()
        
        if raw_roles:
            # Cas 1 : Import CSV (Chaîne "Admin, Manager")
            if isinstance(raw_roles, str):
                role_names = [r.strip() for r in raw_roles.split(',')]
                for name in role_names:
                    try:
                        role = Role.objects.get(name__iexact=name)
                        self._roles_to_add.append(role)
                    except Role.DoesNotExist:
                        print(f"⚠️ Rôle inconnu ignoré : {name}")

            # Cas 2 : API (Liste d'IDs [1, 2])
            elif isinstance(raw_roles, list):
                # On suppose que ce sont des IDs (via PrimaryKeyRelatedField)
                self._roles_to_add = raw_roles
        
        # Si pas de rôles et création, on pourrait mettre un défaut ici
        
        return data

    def save_process(self, data, instance=None):
        # Gestion du mot de passe (inchangée)
        data.pop('password2', None)
        
        if instance:
            data.pop('password', None)
            for attr, value in data.items():
                setattr(instance, attr, value)
            instance.save()
            user = instance
            created = False
        else:
            password = data.pop('password', "DefaultPass123!")
            user = User.objects.create_user(password=password, **data)
            created = True

        return user, created

    def after_save(self, instance, created):
        """
        C'est ici qu'on sauvegarde le ManyToMany (après que l'ID User existe)
        """
        if hasattr(self, '_roles_to_add') and self._roles_to_add:
            # On remplace les anciens rôles ou on ajoute ? 
            # Ici on set() pour remplacer (plus propre pour un save complet)
            instance.roles.set(self._roles_to_add)