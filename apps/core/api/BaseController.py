# apps/core/api/controllers/BaseController.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.db import transaction
from django.http import Http404

# --- Importe nos classes de sécurité de base ---
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class BaseController(APIView):
    """
    Notre Orchestrateur de base (CUD + R).
    Il gère la séquence : Permissions -> Validation -> Service.
    Il utilise 'custom_exception_handler' pour les erreurs
    et 'success_response' pour les succès.
    """
    
    # --- Classes à définir par les enfants (ex: ProductController) ---
    serializer_class = None
    service_class = None

    # --- Sécurité par défaut ---
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.service_class or not self.serializer_class:
            raise NotImplementedError("Les attributs 'service_class' et 'serializer_class' doivent être définis.")
        self.service = self.service_class()
        self.serializer = self.serializer_class

    # --- MÉTHODE D'AIDE POUR LA RÉPONSE DE SUCCÈS ---
    
    def success_response(self, data, message, status_code):
        """ Formate une réponse de succès standard. """
        return Response({
            "status": "success",
            "message": message,
            "data": data
        }, status=status_code)

    # --- MÉTHODES API ---

    def list(self, request, *args, **kwargs):
        """ GET /api/Product/list/ """
        queryset = self.service.list()
        data = self.serializer(queryset, many=True).data
        return self.success_response(data, "Données récupérées avec succès.", status.HTTP_200_OK)

    def retrieve(self, request, pk, *args, **kwargs):
        """ GET /api/Product/retrieve/1/ """
        # get_by_id lève 404, notre handler l'attrape
        instance = self.service.get_by_id(pk) 
        data = self.serializer(instance).data
        return self.success_response(data, "Donnée récupérée avec succès.", status.HTTP_200_OK)

    def save(self, request, pk=None, *args, **kwargs):
        """
        POST /api/Product/save/ (création)
        POST /api/Product/save/1/ (mise à jour)
        """
        instance = None
        if pk:
            # get_by_id lève 404, notre handler l'attrape
            instance = self.service.get_by_id(pk) 
        
        # is_valid lève 400 (ValidationError), notre handler l'attrape
        serializer = self.serializer(instance, data=request.data, partial=bool(instance))
        serializer.is_valid(raise_exception=True) 
        validated_data = serializer.validated_data

        try:
            with transaction.atomic():
                if instance:
                    result = self.service.update(instance, validated_data)
                    message = "Modification effectuée avec succès."
                    status_code = status.HTTP_200_OK
                else:
                    result = self.service.create(validated_data)
                    message = "Création effectuée avec succès."
                    status_code = status.HTTP_201_CREATED
        except Exception as e:
            # Attrape les erreurs "métier" (ex: "Stock insuffisant")
            # et les transforme en erreur 400 gérée par notre handler
            raise exceptions.ValidationError(str(e))

        # Réponse de succès
        data = self.serializer(result).data
        return self.success_response(data, message, status_code)

    def delete(self, request, pk, *args, **kwargs):
        """ POST /api/Product/delete/1/ """
        instance = self.service.get_by_id(pk) 
        result = self.service.delete(instance) 
        
        return self.success_response(result, "Suppression effectuée avec succès.", status.HTTP_200_OK)