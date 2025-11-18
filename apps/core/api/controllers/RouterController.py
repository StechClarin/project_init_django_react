# apps/core/api/controllers/RouterController.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils.module_loading import import_string
from django.apps import apps
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class RouterView(APIView):
    """
    Le Front Controller (Aiguilleur) de notre API (CUD Uniquement).
    Analyse l'URL (/api/Model/method/) et délègue au bon Controller.
    Il n'accepte que les requêtes POST.
    """
    
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def _get_controller_instance(self, model_name):
        controller_name = f"{model_name.capitalize()}Controller"
        for app_config in apps.get_app_configs():
            if app_config.name.startswith('apps.'):
                controller_path = f"{app_config.name}.api.controllers.{model_name.lower()}_controller.{controller_name}"
                try:
                    controller_class = import_string(controller_path)
                    return controller_class()
                except ImportError:
                    continue
        raise Http404(f"Contrôleur '{controller_name}' non trouvé.")

    def _dispatch_request(self, request, model_name, method_name, pk=None):
        try:
            controller = self._get_controller_instance(model_name)
            
            # --- GESTION SPÉCIALE POUR L'AUTH ---
            if model_name.lower() == 'auth':
                # On ne vérifie pas les permissions pour le AuthController
                pass
            else:
                # Pour tous les autres, on vérifie les permissions
                self.check_permissions(request)

            if not hasattr(controller, method_name):
                return Response(
                    {"detail": f"Méthode '{method_name}' non autorisée sur '{model_name}'."},
                    status=status.HTTP_405_METHOD_NOT_ALLOWED
                )
                
            method_to_call = getattr(controller, method_name)

            if pk:
                return method_to_call(request, pk=pk)
            else:
                return method_to_call(request)

        except Http404 as e:
            return Response({"detail": str(e)}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            if hasattr(e, 'detail'):
                return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    # --- MÉTHODE HTTP (POST UNIQUEMENT) ---

    def post(self, request, model_name, method_name, pk=None):
        """ Gère les écritures (save, delete, etc.) """
        # La méthode 'get' est supprimée. 
        # APIView renverra 405 Method Not Allowed si quelqu'un essaie un GET.
        return self._dispatch_request(request, model_name, method_name, pk)
