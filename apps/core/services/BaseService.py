from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404
from django.db import transaction
from apps.core.utils.importfile import ImportFile
from apps.core.utils.exportfile import ExportFile

class BaseService:
    """
    Service de base (Cœur Logique).
    
    Responsabilités :
    1. CRUD standard (List, Get, Save, Delete).
    2. Orchestration de sauvegarde (Hooks before/after).
    3. Import/Export générique et intelligent.
    
    Les services enfants (ex: ProductService) doivent hériter de cette classe.
    """
    
    # Le modèle Django ciblé (à définir dans l'enfant, ex: model = Product)
    model = None 
    
    # Configuration de l'Export : liste des champs (ex: ['name', 'price'])
    export_fields = [] 
    
    # Configuration de l'Import : liste des champs ou config relations
    # ex: ['name', {'category': {'model': Category, 'search_field': 'name'}}]
    import_fields = []

    # ==========================================================================
    # 1. MÉTHODES DE LECTURE (Read)
    # ==========================================================================

    def list(self, filters=None):
        """
        Récupère une liste d'objets, avec filtrage optionnel.
        """
        if filters:
            return self.model.objects.filter(**filters)
        return self.model.objects.all()

    def get_by_id(self, pk):
        """
        Récupère un objet par son ID. Lève une 404 si non trouvé.
        """
        try:
            return self.model.objects.get(pk=pk)
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404(f"{self.model.__name__} non trouvé")

    # ==========================================================================
    # 2. MÉTHODES D'ÉCRITURE (CUD - Save Flow)
    # ==========================================================================

    def before_validate(self, data, instance=None):
        """
        [HOOK] Exécuté AVANT le Serializer.
        Sert à nettoyer les données brutes (trim, upper case, formatage).
        Doit retourner le dictionnaire 'data' modifié.
        """
        return data

    def save(self, validated_data, instance=None):
        """
        Chef d'orchestre de la sauvegarde.
        Ne pas surcharger cette méthode ! Surchargez les hooks ci-dessous.
        Gère la séquence : Before -> Process (Create/Update) -> After.
        """
        # 1. Hook Avant (Dernière modif des données validées avant écriture)
        validated_data = self.before_save(validated_data, instance)

        # 2. Écriture en base (gère automatiquement Create ou Update)
        obj, created = self.save_process(validated_data, instance)

        # 3. Hook Après (Notifications, Logs, actions asynchrones)
        self.after_save(obj, created)

        return obj

    # --- Les Hooks surchargeables ---

    def before_save(self, data, instance=None):
        """
        [HOOK] À surcharger pour modifier les données juste avant l'écriture BDD.
        Ex: Générer un matricule automatique, crypter une donnée.
        """
        return data

    def save_process(self, data, instance=None):
        """
        Effectue l'écriture réelle en base de données.
        Peut être surchargé pour des cas complexes (ex: User et mot de passe).
        Retourne (instance, boolean_created).
        """
        if instance:
            # Mode Update
            for attr, value in data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance, False # False = Mis à jour
        else:
            # Mode Create
            return self.model.objects.create(**data), True # True = Créé

    def after_save(self, instance, created):
        """
        [HOOK] À surcharger pour les actions post-sauvegarde.
        Ex: Envoyer un email de bienvenue, mettre à jour un cache, Websockets.
        """
        pass

    def delete(self, instance):
        """
        Supprime un objet.
        Retourne un petit rapport.
        """
        instance_id = instance.id
        instance.delete()
        return {"id": instance_id, "status": "deleted"}

    # ==========================================================================
    # 3. IMPORT / EXPORT (Outils de masse)
    # ==========================================================================

    # ... (imports et début de classe inchangés)

    def export_data(self, format_type='csv'):
        """
        Génère un fichier (CSV/Excel) contenant les données.
        Gère le renommage des colonnes (Aliasing) pour les relations.
        """
        # 1. Préparation des champs à demander à la BDD
        fields_to_query = [] # Ce qu'on envoie au .values() de Django
        header_mapping = {}  # Pour renommer les colonnes à la fin (ex: role__name -> role)

        if self.export_fields:
            for field in self.export_fields:
                if isinstance(field, dict):
                    # Cas complexe : {'role__name': 'role'}
                    db_field = list(field.keys())[0]
                    csv_header = field[db_field]
                    
                    fields_to_query.append(db_field)
                    header_mapping[db_field] = csv_header
                else:
                    # Cas simple : 'username'
                    fields_to_query.append(field)
                    header_mapping[field] = field # Pas de changement de nom
        else:
            # Fallback : tous les champs simples
            fields_to_query = [f.name for f in self.model._meta.fields]
            header_mapping = {f: f for f in fields_to_query}

        # 2. Requête optimisée
        # On utilise .values() avec les chemins Django (ex: role__name)
        queryset = self.model.objects.all().values(*fields_to_query)
        
        # 3. Renommage des clés (Mapping)
        # On transforme [{'username': 'toto', 'role__name': 'Admin'}]
        # en          [{'username': 'toto', 'role': 'Admin'}]
        data_list = []
        for row in queryset:
            new_row = {}
            for db_key, value in row.items():
                # On utilise le nom mappé pour le CSV
                new_key = header_mapping.get(db_key, db_key)
                new_row[new_key] = value
            data_list.append(new_row)

        # 4. Génération du fichier
        filename = self.model._meta.verbose_name_plural.lower().replace(' ', '_')
        
        if format_type == 'excel': 
            return ExportFile.to_excel(data_list, filename)
        return ExportFile.to_csv(data_list, filename)

    def relation_in_import(self, field_name, value, config):
        """
        Helper pour résoudre une clé étrangère lors de l'import.
        Ex: Transforme "Manager" en l'objet Role(id=5).
        """
        if not value:
            return None
            
        related_model = config.get('model')
        search_field = config.get('search_field', 'name')
        
        try:
            # Recherche insensible à la casse (iexact)
            query = {f"{search_field}__iexact": str(value).strip()}
            return related_model.objects.get(**query)
        except related_model.DoesNotExist:
            raise ValueError(f"Le {field_name} '{value}' n'existe pas.")
        except Exception as e:
            raise ValueError(f"Erreur sur {field_name}: {str(e)}")

    def import_data(self, file_obj, atomic=False):
        """
        Importe des données depuis un fichier.
        Gère la conversion, la résolution des relations et la création via save().
        """
        raw_data = ImportFile.parse(file_obj)
        created_count = 0
        errors = []
        
        # Analyse de la configuration (Champs simples vs Relations)
        simple_fields = set()
        relation_configs = {}

        if self.import_fields:
            for field in self.import_fields:
                if isinstance(field, dict):
                    # C'est une relation : {'role': {'model': Role...}}
                    key = list(field.keys())[0]
                    relation_configs[key] = field[key]
                else:
                    simple_fields.add(field)
        
        try:
            with transaction.atomic():
                for index, row in enumerate(raw_data):
                    row_num = index + 2 # +1 header, +1 index 0
                    try:
                        data_to_save = {}
                        
                        for key, value in row.items():
                            # Cas 1 : Champ simple autorisé
                            if not self.import_fields or key in simple_fields:
                                data_to_save[key] = value
                            
                            # Cas 2 : Relation configurée (Résolution auto)
                            elif key in relation_configs:
                                config = relation_configs[key]
                                data_to_save[key] = self.relation_in_import(key, value, config)

                        # Appel au flux de sauvegarde complet (Hooks inclus !)
                        self.save(data_to_save, instance=None)
                        created_count += 1
                        
                    except Exception as e:
                        errors.append(f"Ligne {row_num}: {str(e)}")
                        # Si mode atomique strict, on arrête tout à la première erreur
                        if atomic: raise ValueError(str(e))
                        
        except ValueError as e:
             return {"status": "error", "imported": 0, "errors": [str(e)]}

        return {
            "status": "success" if not errors else "partial_success", 
            "imported": created_count, 
            "errors": errors
        }