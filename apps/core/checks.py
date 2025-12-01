from django.core.checks import Error, Tags, register
from django.apps import apps
import importlib

@register(Tags.compatibility)
def check_controllers(app_configs, **kwargs):
    errors = []
    
    # On parcourt tous les modèles enregistrés
    for model in apps.get_models():
        app_label = model._meta.app_label
        model_name = model.__name__
        
        # On ne vérifie que nos apps internes (commençant par 'apps.')
        # Mais attention, app_label est juste le nom court (ex: 'shop', 'core').
        # Il faut vérifier le module de l'app config.
        app_config = apps.get_app_config(app_label)
        if not app_config.name.startswith('apps.'):
            continue
            
        # Ignorer certains modèles techniques si besoin (ex: migrations, permissions auto)
        # Pour l'instant on vérifie tout.
        
        # Construction du chemin théorique du contrôleur
        # Convention: apps.{app_label}.api.controllers.{model_name}_controller
        # Attention: model_name est CamelCase (Product), le fichier est snake_case (product_controller)
        
        # Conversion CamelCase -> snake_case
        import re
        snake_name = re.sub(r'(?<!^)(?=[A-Z])', '_', model_name).lower()
        
        controller_module_path = f"{app_config.name}.api.controllers.{snake_name}_controller"
        controller_class_name = f"{model_name}Controller"
        
        try:
            module = importlib.import_module(controller_module_path)
            if not hasattr(module, controller_class_name):
                errors.append(
                    Error(
                        f"Le contrôleur '{controller_class_name}' est introuvable dans '{controller_module_path}'.",
                        hint=f"Créez la classe {controller_class_name} dans {controller_module_path}.py",
                        obj=model,
                        id='core.E002',
                    )
                )
        except ImportError:
            errors.append(
                Error(
                    f"Le fichier contrôleur pour le modèle '{model_name}' est introuvable.",
                    hint=f"Créez le fichier {controller_module_path}.py",
                    obj=model,
                    id='core.E001',
                )
            )
            
    return errors
