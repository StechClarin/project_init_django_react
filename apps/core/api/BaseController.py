from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class BaseController(APIView):
    serializer_class = None
    service_class = None

    def list(self, request, *args, **kwargs):
        # Permission check here
        
        service = self.service_class()
        queryset = service.get_all()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        # Permission check here
        
        service = self.service_class()
        instance = service.get_by_id(kwargs.get('pk'))
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def save(self, request, *args, **kwargs):
        # Permission check here
        
        service = self.service_class()
        pk = kwargs.get('pk')
        instance = service.get_by_id(pk) if pk else None
        
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            if instance:
                service.update(instance, serializer.validated_data)
            else:
                service.create(serializer.validated_data)
            return Response(serializer.data, status=status.HTTP_201_CREATED if not instance else status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Permission check here
        
        service = self.service_class()
        instance = service.get_by_id(kwargs.get('pk'))
        if not instance:
            return Response(status=status.HTTP_404_NOT_FOUND)
        service.delete(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
