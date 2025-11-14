# Fichier: apps/core/management/commands/craft.py
# VERSION FINALE (Contrôleur-Service + Serializers Séparés)

import os
from pathlib import Path
from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError
from django.apps import apps

# Pluralize helper (simple English, fallback)
def pluralize(word: str) -> str:
    """Very basic pluralization: adds 's' if not already ending with 's'."""
    if word.endswith('s'):
        return word
    return word + 's'

# ----------------------------
# Helpers
# ----------------------------
def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def ensure_file(p: Path, default_content: str = ""):
    if not p.exists():
        p.write_text(default_content, encoding="utf-8")

def append_unique_line(p: Path, line: str):
    ensure_file(p, "")
    content = p.read_text(encoding="utf-8")
    if line not in content:
        p.write_text(content + ("" if content.endswith("\n") else "\n") + line + "\n", encoding="utf-8")


class Command(BaseCommand):
    help = "Couteau-suisse: génère modèles, serializers, contrôleurs, services, etc. (Architecture Contrôleur-Service)"

    def add_arguments(self, parser):
        sub = parser.add_subparsers(dest='command', required=True)

        aprep = sub.add_parser('app:prepare', help="Prépare l'arborescence (models/, api/, services/)")
        aprep.add_argument('app_name', type=str, help="Nom de l'app (ex: core)")

        m = sub.add_parser('model', help='Crée un modèle dans models/<Model>.py')
        m.add_argument('model_name', type=str, help="Nom du modèle (ex: Product)")
        m.add_argument('app_name', type=str, help="Nom de l'app (ex: products)")

        # --- MODIFIÉ ---
        s = sub.add_parser('serializer', help='Crée un fichier ModelSerializer dans api/serializers/')
        s.add_argument('model_name', type=str, help="Nom du modèle à sérialiser (ex: Product)")
        s.add_argument('app_name', type=str, help="Nom de l'app (ex: products)")

        c = sub.add_parser('controller', help='Crée un Controller qui hérite de BaseController')
        c.add_argument('model_name', type=str, help="Nom du modèle pour le Controller (ex: Product)")
        c.add_argument('app_name', type=str, help="Nom de l'app (ex: products)")

        serv = sub.add_parser('service', help='Crée un Service qui hérite de BaseService')
        serv.add_argument('model_name', type=str, help="Nom du modèle pour le Service (ex: Product)")
        serv.add_argument('app_name', type=str, help="Nom de l'app (ex: products)")

        sc = sub.add_parser('scaffold', help='Scaffold: model + serializer + controller + service + migrate')
        sc.add_argument('model_name', type=str, help="ex: Product")
        sc.add_argument('app_name', type=str, help="ex: products")
        
        am = sub.add_parser('automigrate', help='Crée et applique les migrations')
        am.add_argument('app_name', nargs='?', default=None, help="Nom de l'app (ex: users)")
        am.add_argument('--name', type=str)
        
        fr = sub.add_parser('fresh', help="Réinitialise les migrations d'une app")
        fr.add_argument('app_name', type=str, help="Nom de l'app (ex: users)")

    # ----------------------------
    # DRF prereq
    # ----------------------------
    def _check_drf(self):
        try:
            import rest_framework
        except Exception:
            raise CommandError("Installe 'djangorestframework' pour utiliser les commandes API.")

    # ----------------------------
    # Arborescence
    # ----------------------------
    def _prepare_app_layout(self, app_name_simple: str, *, create_bridge=True):
        try:
            app_dir = Path(apps.get_app_config(app_name_simple).path)
        except LookupError:
            raise CommandError(f"L'app '{app_name_simple}' n'existe pas ou n'est pas installée dans INSTALLED_APPS.")

        models_dir = app_dir / "models"
        api_dir = app_dir / "api"
        api_controllers_dir = api_dir / "controllers"
        services_dir = app_dir / "services"
        
        # --- MODIFIÉ ---
        api_serializers_dir = api_dir / "serializers" # Dossier au lieu de fichier

        # --- MODIFIÉ ---
        for d in [models_dir, api_dir, api_controllers_dir, services_dir, api_serializers_dir]:
            ensure_dir(d)
            ensure_file(d / "__init__.py", "")

        # --- SUPPRIMÉ ---
        # ensure_file(api_serializers_file, f"# Fichier généré pour {app_name_simple}\nfrom apps.core.api.serializers.BaseSerializer import BaseSerializer\n")
        
        if create_bridge:
            bridge = app_dir / "models.py" 
            if not bridge.exists():
                bridge.write_text(f"# Bridge pour les modèles dans le dossier /models\nfrom .models import * # noqa\n", encoding="utf-8")
                self.stdout.write(self.style.SUCCESS(f"✔ Bridge créé: {bridge}"))
            else:
                append_unique_line(bridge, "from .models import * # noqa")

        return {
            "app_dir": app_dir,
            "models_dir": models_dir,
            "api_dir": api_dir,
            "api_controllers_dir": api_controllers_dir,
            "services_dir": services_dir,
            "api_serializers_dir": api_serializers_dir, # --- MODIFIÉ ---
        }

    # ----------------------------
    # Templates
    # ----------------------------
    def _tpl_model(self, model_name: str) -> str:
        # (Inchangé)
        model_name_lower = model_name.lower()
        return f"""from django.db import models

class {model_name}(models.Model):
    name = models.CharField(max_length=150, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "{model_name_lower}"
        verbose_name_plural = "{pluralize(model_name_lower)}"
        ordering = ['-created_at']

    def __str__(self):
        return self.name or f"{model_name} #{{self.pk}}"
"""

    def _tpl_models_init_line(self, model_name: str) -> str:
        # (Inchangé)
        return f"from .{model_name.lower()} import {model_name}"

    def _tpl_serializer(self, model_name: str) -> str:
        # (Inchangé - il est déjà correct pour un fichier unique)
        return f"""
from apps.core.api.serializers.BaseSerializer import BaseSerializer
from ...models import {model_name}

class {model_name}Serializer(BaseSerializer):
    class Meta:
        model = {model_name}
        fields = "__all__"
"""
    
    # --- NOUVEAU TEMPLATE ---
    def _tpl_serializer_init_line(self, model_name: str) -> str:
        """Génère la ligne pour le __init__.py du dossier serializers."""
        file_name = f"{model_name.lower()}_serializer"
        class_name = f"{model_name}Serializer"
        return f"from .{file_name} import {class_name}"

    def _tpl_controller(self, model_name: str, app_name: str) -> str:
        # --- MODIFIÉ ---
        # Correction de l'import pour pointer vers le fichier spécifique
        return f"""from apps.core.api.controllers.BaseController import BaseController
from ..serializers.{model_name.lower()}_serializer import {model_name}Serializer
from ...services.{model_name.lower()}_service import {model_name}Service

class {model_name}Controller(BaseController):
    serializer_class = {model_name}Serializer
    service_class = {model_name}Service
"""

    def _tpl_service(self, model_name: str) -> str:
        # (Inchangé - il est déjà correct)
        return f"""from apps.core.services.BaseService import BaseService
from ..models import {model_name}

class {model_name}Service(BaseService):
    model = {model_name}

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
"""

    # ----------------------------
    # Handle
    # ----------------------------
    def handle(self, *args, **opt):
        cmd = opt['command']
        
        app_name_arg = opt.get('app_name')
        app_name_simple = app_name_arg.split('.')[-1] if app_name_arg else None
        
        if cmd == 'app:prepare':
            # (Inchangé)
            self._prepare_app_layout(app_name_simple)
            self.stdout.write(self.style.SUCCESS(f"✔ Arborescence prête pour '{app_name_simple}'"))
            return

        if cmd == 'model':
            # (Inchangé)
            model_name = opt['model_name'].capitalize()
            layout = self._prepare_app_layout(app_name_simple)
            file = layout['models_dir'] / f"{model_name.lower()}.py"
            if file.exists():
                raise CommandError(f"Le modèle '{model_name}' existe déjà: {file}")
            
            file.write_text(self._tpl_model(model_name), encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"✔ Modèle créé: {file}"))
            
            append_unique_line(layout['models_dir'] / "__init__.py", self._tpl_models_init_line(model_name))
            self.stdout.write(self.style.SUCCESS(f"✔ Ajout dans models/__init__.py"))
            return

        if cmd == 'serializer':
            # --- MODIFIÉ ---
            # Logique pour créer un fichier séparé
            self._check_drf()
            model_name = opt['model_name'].capitalize()
            layout = self._prepare_app_layout(app_name_simple, create_bridge=False)
            
            file_name = f"{model_name.lower()}_serializer.py"
            file_path = layout['api_serializers_dir'] / file_name
            
            if file_path.exists():
                raise CommandError(f"Le Serializer '{model_name}' existe déjà: {file_path}")

            file_path.write_text(self._tpl_serializer(model_name), encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"✔ Serializer créé: {file_path}"))
            
            # Ajout au __init__.py du dossier serializers
            append_unique_line(
                layout['api_serializers_dir'] / "__init__.py", 
                self._tpl_serializer_init_line(model_name)
            )
            self.stdout.write(self.style.SUCCESS(f"✔ Ajout dans api/serializers/__init__.py"))
            return

        if cmd == 'controller':
            # (Inchangé)
            self._check_drf()
            model_name = opt['model_name'].capitalize()
            layout = self._prepare_app_layout(app_name_simple, create_bridge=False)
            file_name = f"{model_name.lower()}_controller.py"
            file_path = layout['api_controllers_dir'] / file_name
            if file_path.exists():
                raise CommandError(f"Le Controller '{model_name}' existe déjà: {file_path}")
            file_path.write_text(self._tpl_controller(model_name, app_name_simple), encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"✔ Controller créé: {file_path}"))
            return

        if cmd == 'service':
            # (Inchangé)
            model_name = opt['model_name'].capitalize()
            layout = self._prepare_app_layout(app_name_simple, create_bridge=False)
            file_name = f"{model_name.lower()}_service.py"
            file_path = layout['services_dir'] / file_name
            if file_path.exists():
                raise CommandError(f"Le Service '{model_name}' existe déjà: {file_path}")
            file_path.write_text(self._tpl_service(model_name), encoding="utf-8")
            self.stdout.write(self.style.SUCCESS(f"✔ Service créé: {file_path}"))
            return

        if cmd == 'scaffold':
            # (Inchangé)
            model_name = opt['model_name'].capitalize()
            self.stdout.write(self.style.NOTICE(f"--- Début du Scaffold pour {model_name} ---"))
            
            self.stdout.write(self.style.NOTICE("• Génération du Modèle..."))
            call_command('craft', 'model', model_name, app_name_simple)
            
            self.stdout.write(self.style.NOTICE("• Génération du Serializer..."))
            call_command('craft', 'serializer', model_name, app_name_simple)
            
            self.stdout.write(self.style.NOTICE("• Génération du Service..."))
            call_command('craft', 'service', model_name, app_name_simple)
            
            self.stdout.write(self.style.NOTICE("• Génération du Controller..."))
            call_command('craft', 'controller', model_name, app_name_simple)
            
            self.stdout.write(self.style.NOTICE("• Génération et application des migrations..."))
            call_command('craft', 'automigrate', app_name_simple, '--name', f"create_{model_name.lower()}_model")
            
            self.stdout.write(self.style.SUCCESS(f"✔ Scaffold terminé pour {model_name}"))
            return

        if cmd == 'automigrate':
            # (Inchangé)
            mk = ['makemigrations']
            if app_name_simple:
                mk.append(app_name_simple)
            if opt.get('name'):
                mk.append('--name')
                mk.append(opt['name'])
            call_command(*mk)
            call_command('migrate', *( [app_name_simple] if app_name_simple else [] ))
            self.stdout.write(self.style.SUCCESS("✔ Makemigrations + Migrate OK."))
            return
            
        if cmd == 'fresh':
            # (Inchangé)
            try:
                app_dir = Path(apps.get_app_config(app_name_simple).path)
            except LookupError:
                raise CommandError(f"L'app '{app_name_simple}' n'existe pas.")
            
            mig_dir = app_dir / "migrations"
            if mig_dir.exists():
                for f in mig_dir.iterdir():
                    if f.name != "__init__.py" and f.suffix.lower() in [".py", ".pyc"]:
                        f.unlink()
                        self.stdout.write(f"  - supprimé: {f.name}")
            
            call_command('makemigrations', app_name_simple)
            call_command('migrate', app_name_simple)
            self.stdout.write(self.style.SUCCESS(f"✔ Fresh migrations OK pour '{app_name_simple}'."))
            return