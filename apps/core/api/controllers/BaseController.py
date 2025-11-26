from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.db import transaction
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class BaseController(APIView):
    """
    Notre Orchestrateur de base (CUD Uniquement).
    Il gère la séquence : 
    Permissions -> Préparation (before_validate) -> Validation -> Service (save).
    """
    
    serializer_class = None
    service_class = None
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.service_class or not self.serializer_class:
            raise NotImplementedError("Les attributs 'service_class' et 'serializer_class' doivent être définis.")
        self.service = self.service_class()
        self.serializer = self.serializer_class

    # --- HELPER POUR RÉPONSE STANDARD ---
    def success_response(self, data, message, status_code):
        return Response({
            "status": "success",
            "message": message,
            "data": data
        }, status=status_code)

    # --- MÉTHODES CUD (Orchestration) ---

    def save(self, request, pk=None, *args, **kwargs):
        """
        Logique unifiée pour Création (POST /) et Modification (POST /id/).
        """
        instance = None
        if pk:
            instance = self.service.get_by_id(pk)
        
        # 1. PRÉPARATION (Service)
        # On laisse le service nettoyer les données brutes (ex: trim, upper, formatage)
        # On utilise .copy() pour éviter de modifier la request.data immuable
        raw_data = request.data.copy() if hasattr(request.data, 'copy') else request.data
        prepared_data = self.service.before_validate(raw_data, instance)

        # 2. VALIDATION (Serializer)
        # On valide les données préparées
        serializer = self.serializer(instance, data=prepared_data, partial=bool(instance))
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # 3. EXÉCUTION (Service)
        try:
            with transaction.atomic():
                # On délègue tout au service (qui gère create vs update et les hooks)
                result = self.service.save(validated_data, instance)
                
                # Définition du message de succès
                if instance:
                    status_code = status.HTTP_200_OK
                    message = "Modification effectuée avec succès."
                else:
                    status_code = status.HTTP_201_CREATED
                    message = "Création effectuée avec succès."

        except Exception as e:
            # On renvoie une erreur 400 propre
            # (Notre CustomExceptionHandler peut aussi l'attraper si on le laisse lever)
            if hasattr(e, 'detail'):
                raise e # Laisse passer les erreurs DRF
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # 4. RÉPONSE
        data = self.serializer(result).data
        return self.success_response(data, message, status_code)

    def delete(self, request, pk, *args, **kwargs):
        """ Logique pour la suppression """
        instance = self.service.get_by_id(pk)
        
        try:
            result = self.service.delete(instance)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
        return self.success_response(result, "Suppression effectuée avec succès.", status.HTTP_200_OK)