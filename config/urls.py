from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.core.api.controllers.RouterController import RouterView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from graphene_django.views import GraphQLView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path(
        "api/<str:model_name>/<str:method_name>/", 
        RouterView.as_view(), 
        name="api_router"
    ),
    path(
        "api/<str:model_name>/<str:method_name>/<int:pk>/", 
        RouterView.as_view(), 
        name="api_router_pk"
    ),
    
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]