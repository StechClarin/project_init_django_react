# Fichier: apps/core/management/commands/seed_access.py
from django.core.management.base import BaseCommand
# On importe depuis 'core' car c'est là qu'on a mis les modèles
from apps.core.models import Group, Permission 
# TA STRUCTURE DE SEED (CORRIGÉE)
GROUP_STRUCTURE = [
    {
        "name": "Gestion des Utilisateurs",
        "tag": "user", # Le tag correspond à la page "user"
        "permissions": [
            {"name": "Lire les utilisateurs", "codename": "view_user"},
            {"name": "Ajouter un utilisateur", "codename": "add_user"},
            {"name": "Modifier un utilisateur", "codename": "change_user"},
            {"name": "Supprimer un utilisateur", "codename": "delete_user"},
        ]
    },
    {
        "name": "Gestion des Rôles",
        "tag": "role", # Le tag correspond à la page "Role"
        "permissions": [
            {"name": "Lire les rôles", "codename": "view_role"},
            {"name": "Ajouter un rôle", "codename": "add_role"},
            {"name": "Modifier un rôle", "codename": "change_role"},
            {"name": "Supprimer un rôle", "codename": "delete_role"},
        ]
    },
    # --- AJOUTE TES AUTRES GROUPES ET PERMISSIONS ICI ---
]

class Command(BaseCommand):
    help = "Crée les Permissions et les Groupes selon la structure définie."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("--- Début du seeding Access (Permissions & Groups) ---"))
        
        for group_data in GROUP_STRUCTURE:
            group_name = group_data['name']
            tag = group_data['tag']
            
            group, created = Group.objects.get_or_create(name=group_name)
            if created:
                self.stdout.write(f"  Groupe '{group_name}' créé.")
            
            group.permissions.clear()
            
            for perm_data in group_data['permissions']:
                perm, p_created = Permission.objects.get_or_create(
                    codename=perm_data['codename'],
                    defaults={'name': perm_data['name'], 'tag': tag}
                )
                
                if p_created:
                    self.stdout.write(f"    Permission '{perm.codename}' créée.")
                
                group.permissions.add(perm)

            self.stdout.write(self.style.SUCCESS(f"  ✔ Permissions pour '{group_name}' synchronisées."))

        self.stdout.write(self.style.SUCCESS("--- Seeding Access terminé ---"))