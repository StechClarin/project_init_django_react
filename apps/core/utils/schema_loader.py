# apps/core/utils/schema_loader.py
import inspect
import pkgutil
import importlib
from pathlib import Path
from django.apps import apps
from django.conf import settings
import graphene

def load_all_queries():
    """
    Scanne toutes les applications installées pour trouver automatiquement
    les classes Query définies dans 'graphql/Queries'.
    Retourne une liste de classes.
    """
    queries = []
    
    # On parcourt toutes les configs d'apps (core, users, products...)
    for app_config in apps.get_app_configs():
        # On ne s'intéresse qu'à nos apps locales (dans le dossier 'apps')
        if not app_config.name.startswith('apps.'):
            continue
            
        # Chemin théorique du package Queries : apps.monapp.graphql.Queries
        queries_package_name = f"{app_config.name}.graphql.Queries"
        
        try:
            # On essaie d'importer le package (dossier)
            queries_module = importlib.import_module(queries_package_name)
        except ImportError:
            # Si le dossier n'existe pas, on passe à l'app suivante
            continue

        # On parcourt tous les fichiers .py dans ce dossier
        if hasattr(queries_module, "__path__"):
            for _, name, _ in pkgutil.iter_modules(queries_module.__path__):
                # Importe le module (ex: apps.users.graphql.Queries.user_query)
                full_module_name = f"{queries_package_name}.{name}"
                module = importlib.import_module(full_module_name)
                
                # On inspecte le fichier pour trouver la classe Query
                for member_name, member_obj in inspect.getmembers(module):
                    if (inspect.isclass(member_obj) 
                        and member_name.endswith("Query") 
                        and member_obj is not graphene.ObjectType
                        and issubclass(member_obj, graphene.ObjectType)):
                        
                        # Bingo ! On a trouvé une classe Query (ex: UserQuery)
                        queries.append(member_obj)

    return queries