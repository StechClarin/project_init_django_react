# projet_init/urls.py
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

# --- Importe notre Aiguilleur (Sécurisé) ---
from apps.core.api.controllers.RouterController import RouterView

# --- Importe les vues de Login (Publiques) ---
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# --- Importe la vue GraphQL ---
from graphene_django.views import GraphQLView

urlpatterns = [
    # 1. L'admin de base
    path('admin/', admin.site.urls),

    # 2. L'API DE CONNEXION (PUBLIQUE)
    #    On la met AVANT le routeur générique.
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 3. NOTRE API D'ÉCRITURE CUD (SÉCURISÉE)
    #    Elle capture tout le reste.
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
    
    # 4. NOTRE API DE LECTURE (GraphQL)
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
]