# apps/profilmanagement/models/user.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .role import Role
from .user_manager import UserManager # <-- On importe notre Manager

class User(AbstractBaseUser, PermissionsMixin):
    """
    Modèle User personnalisé hérite de AbstractBaseUser.
    N'inclut PAS les champs 'groups' or 'user_permissions' de Django.
    """
    username = models.CharField(max_length=150, unique=True, verbose_name="Nom d'utilisateur")
    email = models.EmailField(unique=True, verbose_name="Adresse email")
    first_name = models.CharField(max_length=150, blank=True, verbose_name="Prénom")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Nom de famille")

    is_staff = models.BooleanField(default=False, help_text="Permet d'accéder au site admin Django.")
    is_active = models.BooleanField(default=True, help_text="Désigne si cet utilisateur doit être traité comme actif.")
    date_joined = models.DateTimeField(auto_now_add=True)

    # --- NOTRE LOGIQUE MÉTIER ---
    role = models.ForeignKey(
        Role,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Rôle",
    )

    # --- Configuration du Manager ---
    objects = UserManager() # On dit à Django d'utiliser notre manager

    # --- Champs requis par Django ---
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email'] # Champs demandés par 'createsuperuser'

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"

    def __str__(self):
        return self.username

    # On doit aussi supprimer les 'related_name' de 'groups' et 'user_permissions'
    # que 'PermissionsMixin' pourrait ajouter, en les écrasant.
    groups = None
    user_permissions = None