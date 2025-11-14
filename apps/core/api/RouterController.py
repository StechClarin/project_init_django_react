from django.urls import resolve
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from importlib import import_module

class RouterController(APIView):
    def dispatch(self, request, *args, **kwargs):
        model_name = kwargs.get("model_name")
        method_name = kwargs.get("method_name")

        try:
            # Dynamically import the controller
            module_path = f"apps.{model_name.lower()}s.api.controllers.{model_name.lower()}_controller"
            module = import_module(module_path)
            controller_class = getattr(module, f"{model_name.capitalize()}Controller")
            
            # Instantiate the controller and call the method
            controller_instance = controller_class()
            method = getattr(controller_instance, method_name)
            
            return method(request, *args, **kwargs)
            
        except (ImportError, AttributeError) as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
