# apps/core/api/controllers/BaseController.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class BaseController(APIView):
    """
    Notre Orchestrateur de base (CUD Uniquement).
    Il gère la séquence : Permissions -> Validation -> Service.
    Il ne gère PAS la lecture (GET), qui est déléguée à GraphQL.
    """
    
    serializer_class = None
    service_class = None
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated] # Sécurisé par défaut

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.service_class or not self.serializer_class:
            raise NotImplementedError("Les attributs 'service_class' et 'serializer_class' doivent être définis.")
        self.service = self.service_class()
        self.serializer = self.serializer_class

    # --- MÉTHODES CUD (Orchestration) ---

    def save(self, request, pk=None, *args, **kwargs):
        """
        Logique pour POST /api/Product/save/ (création)
        Logique pour POST /api/Product/save/1/ (mise à jour)
        """
        instance = None
        if pk:
            instance = self.service.get_by_id(pk)
        
        serializer = self.serializer(instance, data=request.data, partial=bool(instance))
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        try:
            with transaction.atomic():
                if instance:
                    result = self.service.update(instance, validated_data)
                    status_code = status.HTTP_200_OK
                else:
                    result = self.service.create(validated_data)
                    status_code = status.HTTP_201_CREATED
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        data = self.serializer(result).data
        return Response(data, status=status_code)

    def delete(self, request, pk, *args, **kwargs):
        """ Logique pour POST /api/Product/delete/1/ """
        instance = self.service.get_by_id(pk)
        result = self.service.delete(instance)
        return Response(result, status=status.HTTP_200_OK)