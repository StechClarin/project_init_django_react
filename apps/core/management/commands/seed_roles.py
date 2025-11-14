# Fichier: apps/core/management/commands/seed_roles.py

import os
from django.core.management.base import BaseCommand
from apps.profilmanagement.models import Role, User
from apps.core.models import Group # On importe Group depuis 'core'
from django.db import IntegrityError

class Command(BaseCommand):
    help = "Crée les Rôles, les lie aux Groupes, et crée le super-admin par défaut."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("--- Début du seeding des Rôles ---"))
        
        # 1. Gestion du Rôle "Admin" (tous les droits)
        self.stdout.write(self.style.NOTICE("--- Configuration du Rôle Admin ---"))
        
        admin_role, created = Role.objects.get_or_create(name="Admin")
        if created:
            self.stdout.write("  Rôle 'Admin' créé.")
            
        # On lui donne TOUS les groupes (donc toutes les permissions)
        all_groups = Group.objects.all()
        admin_role.groups.set(all_groups)
        self.stdout.write(f"  ✔ Rôle 'Admin' synchronisé avec {all_groups.count()} groupes.")
        
        # 2. CRÉATION DE TON SUPER-UTILISATEUR "ethernanos"
        self.stdout.write(self.style.NOTICE("--- Création du Super-Admin 'ethernanos' ---"))
        
        # On lit le mot de passe depuis le .env (SÉCURISÉ)
        admin_pass = os.environ.get('ADMIN_DEFAULT_PASSWORD')
        if not admin_pass or admin_pass == "admin": # Sécurité
            self.stdout.write(self.style.ERROR("[ERREUR] ADMIN_DEFAULT_PASSWORD n'est pas défini ou est trop faible dans le .env !"))
            self.stdout.write(self.style.WARNING("  Veuillez le définir sur 'admin' (ou autre) dans votre .env."))
            return

        try:
            # On cherche par 'username'
            if not User.objects.filter(username='ethernanos').exists():
                admin_user = User.objects.create_superuser(
                    username='ethernanos',
                    email='ethernanos@gmail.com',
                    password=admin_pass,
                    role=admin_role # On assigne le rôle Admin
                )
                self.stdout.write(self.style.SUCCESS("  ✔ Utilisateur 'ethernanos' créé avec succès."))
            else:
                # S'il existe, on s'assure qu'il a le bon rôle
                admin_user = User.objects.get(username='ethernanos')
                admin_user.role = admin_role
                admin_user.is_superuser = True
                admin_user.is_staff = True
                admin_user.save()
                self.stdout.write(self.style.WARNING("  ✔ Utilisateur 'ethernanos' existe déjà. Rôle Admin assigné/mis à jour."))

        except IntegrityError:
            self.stdout.write(self.style.WARNING("  ✔ Utilisateur 'ethernanos' existe déjà."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"  [ERREUR] {e}"))
            
        self.stdout.write(self.style.SUCCESS("--- Seeding Rôles terminé ---"))