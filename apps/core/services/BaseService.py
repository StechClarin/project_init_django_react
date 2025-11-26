# apps/core/services/BaseService.py
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import Http404
from django.db import transaction
from apps.core.utils.importfile import ImportFile
from apps.core.utils.exportfile import ExportFile

class BaseService:
    """
    Service de base V2 : Architecture 'Save Flow'
    Fusionne Create et Update en un seul flux logique avec des Hooks.
    """
    model = None 
    export_fields = [] 
    import_fields = []

    # --- LECTURE (R) ---

    def list(self, filters=None):
        if filters:
            return self.model.objects.filter(**filters)
        return self.model.objects.all()

    def get_by_id(self, pk):
        try:
            return self.model.objects.get(pk=pk)
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404(f"{self.model.__name__} non trouvé")

    # --- ÉCRITURE (CUD - Save Flow) ---

    def save(self, validated_data, instance=None):
        """
        Méthode principale d'orchestration.
        Ne pas surcharger celle-ci, surcharger les hooks !
        """
        # 1. Hook Avant (Formatage, calculs préliminaires)
        validated_data = self.before_save(validated_data, instance)

        # 2. Processus de Sauvegarde (Create ou Update)
        # Retourne (instance, created_boolean)
        obj, created = self.save_process(validated_data, instance)

        # 3. Hook Après (Notifications, relations tierces)
        self.after_save(obj, created)

        return obj

    # --- LES HOOKS SURCHARGEABLES ---

    def before_save(self, data, instance=None):
        """
        À surcharger pour modifier les données AVANT la sauvegarde.
        Ex: Générer un matricule, forcer une majuscule.
        Doit retourner les données.
        """
        return data

    def save_process(self, data, instance=None):
        """
        Effectue l'écriture en base.
        Peut être surchargé si la méthode de sauvegarde est complexe.
        """
        if instance:
            # Mode Update
            for attr, value in data.items():
                setattr(instance, attr, value)
            instance.save()
            return instance, False # False = Pas créé (mis à jour)
        else:
            # Mode Create
            return self.model.objects.create(**data), True # True = Créé

    def after_save(self, instance, created):
        """
        À surcharger pour les actions APRÈS la sauvegarde.
        Ex: Créer des logs, envoyer des mails, sauvegarder des enfants.
        """
        pass

    def delete(self, instance):
        instance_id = instance.id
        instance.delete()
        return {"id": instance_id, "status": "deleted"}

    # --- IMPORT / EXPORT (Mis à jour pour utiliser save()) ---

    def export_data(self, format_type='csv'):
        # ... (Code export inchangé) ...
        fields_to_export = self.export_fields or [f.name for f in self.model._meta.fields]
        queryset = self.model.objects.all().values(*fields_to_export)
        filename = self.model._meta.verbose_name_plural.lower().replace(' ', '_')
        if format_type == 'excel': return ExportFile.to_excel(list(queryset), filename)
        return ExportFile.to_csv(list(queryset), filename)

    def import_data(self, file_obj, atomic=False):
        # ... (Début code import inchangé) ...
        raw_data = ImportFile.parse(file_obj)
        created_count = 0; errors = []; valid_fields = set(self.import_fields) if self.import_fields else None

        try:
            with transaction.atomic():
                for index, row in enumerate(raw_data):
                    try:
                        data_to_save = {}
                        if valid_fields:
                            for k, v in row.items():
                                if k in valid_fields: data_to_save[k] = v
                        else:
                            data_to_save = row
                        
                        # --- CHANGEMENT ICI : On appelle save() au lieu de create() ---
                        self.save(data_to_save, instance=None) 
                        
                        created_count += 1
                    except Exception as e:
                        errors.append(f"Ligne {index+2}: {str(e)}")
                        if atomic: raise ValueError(str(e))
        except ValueError as e:
             return {"status": "error", "imported": 0, "errors": [str(e)]}

        return {"status": "success" if not errors else "partial", "imported": created_count, "errors": errors}