# apps/core/api/exception_handler.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status, exceptions
from django.http import Http404

def custom_exception_handler(exc, context):
    """
    Notre gestionnaire d'exceptions personnalisé.
    Il intercepte toutes les erreurs et les formate en :
    {
        "status": "error",
        "message": "...",
        "data": { ... }
    }
    """
    
    # On récupère d'abord la réponse d'erreur standard de DRF
    response = exception_handler(exc, context)

    # On définit notre format de réponse d'erreur
    error_payload = {
        "status": "error",
        "message": None,
        "data": None # Pour les erreurs de validation
    }

    # --- On "traduit" les erreurs les plus courantes ---

    if isinstance(exc, Http404):
        error_payload["message"] = "Ressource non trouvée."
        return Response(error_payload, status=status.HTTP_404_NOT_FOUND)

    if isinstance(exc, exceptions.ValidationError):
        # C'est l'erreur la plus importante (serializer.is_valid() a échoué)
        error_payload["message"] = "Les données fournies sont invalides."
        # "exc.detail" contient le dictionnaire des erreurs (ex: {"name": "Ce champ est requis."})
        error_payload["data"] = exc.detail 
        return Response(error_payload, status=status.HTTP_400_BAD_REQUEST)

    if isinstance(exc, (exceptions.NotAuthenticated)):
        error_payload["message"] = "Authentification requise."
        return Response(error_payload, status=status.HTTP_401_UNAUTHORIZED)
    
    if isinstance(exc, (exceptions.AuthenticationFailed)):
        error_payload["message"] = "Authentification échouée (token invalide ou expiré)."
        return Response(error_payload, status=status.HTTP_401_UNAUTHORIZED)
    
    if isinstance(exc, (exceptions.PermissionDenied)):
        error_payload["message"] = "Permission refusée."
        return Response(error_payload, status=status.HTTP_403_FORBIDDEN)

    # Si c'est une erreur serveur inconnue (500)
    if response is None:
        error_payload["message"] = "Une erreur interne du serveur est survenue."
        return Response(error_payload, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Pour toutes les autres erreurs gérées par DRF
    error_payload["message"] = response.data.get("detail", "Une erreur est survenue.")
    return Response(error_payload, status=response.status_code)