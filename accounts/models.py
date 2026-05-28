from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Manager personnalise pour le modele User"""
    
    def create_user(self, email, password=None, **extra_fields):
        """Cree un utilisateur standard"""
        if not email:
            raise ValueError("L'adresse email est obligatoire.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Cree un superutilisateur"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        extra_fields.setdefault("is_active", True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modele User personnalise avec roles
    Remplace le User par defaut de Django
    Utilise email comme identifiant principal
    """
    
    class Role(models.TextChoices):
        ADMIN = "admin", "Administrateur"
        MANAGER = "manager", "Manager"
        EDITOR = "editor", "Editeur"
        VIEWER = "viewer", "Consultation"
        STUDENT = "student", "Etudiant"

    # CHAMPS PRINCIPAUX
    email = models.EmailField(
        unique=True,
        db_index=True,
        help_text="Adresse email unique"
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Prenom"
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        help_text="Nom"
    )
    
    # ROLE AVEC DEFAULT
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.VIEWER,
        db_index=True,
        help_text="Role de l'utilisateur"
    )
    
    # STATUT
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Utilisateur actif"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Acces admin"
    )
    email_verified = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Email verifie"
    )
    
    # INFORMATIONS PERSONNELLES
    phone = models.CharField(
        max_length=30, 
        blank=True, 
        null=True)
    
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="Date de naissance"
    )
    bio = models.TextField(
        blank=True,
        help_text="Biographie"
    )
    avatar = models.ImageField(
        upload_to="avatars/%Y/%m/",
        blank=True,
        null=True,
        help_text="Photo de profil"
    )
    
    # DATES
    date_joined = models.DateTimeField(
        default=timezone.now,   
        db_index=True,
        help_text="Date d'inscription"
    )
    last_login = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Derniere connexion"
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"
        ordering = ["-date_joined"]
        indexes = [
            models.Index(fields=["email", "is_active"]),
            models.Index(fields=["role", "is_active"]),
        ]

    def __str__(self):
        return self.email 

    def get_full_name(self):
        """Retourne le nom complet"""
        return f"{self.first_name} {self.last_name}".strip() or self.email

    def get_short_name(self):
        """Retourne le prenom"""
        return self.first_name or self.email

    @property
    def is_admin(self):
        """Verifie si l'utilisateur est admin"""
        return self.role == self.Role.ADMIN or self.is_superuser

    def has_role(self, *roles):
        """Verifie si l'utilisateur a un des roles"""
        return self.role in roles or self.is_superuser
    
    def is_manager(self):
        """Verifie si manager"""
        return self.role in [self.Role.ADMIN, self.Role.MANAGER]
    
    def is_editor(self):
        """Verifie si editeur"""
        return self.role in [self.Role.ADMIN, self.Role.MANAGER, self.Role.EDITOR]


class Profile(models.Model):
    """
    Profil utilisateur avec infos supplementaires
    Relation OneToOne avec User
    """
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name="Utilisateur"
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Adresse"
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text="Ville"
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        help_text="Pays"
    )
    zip_code = models.CharField(
        max_length=20,
        blank=True,
        help_text="Code postal"
    )
    
    # DATES
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Date de creation"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Date de modification"
    )

    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profils"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Profil de {self.user.email}"


class LoginHistory(models.Model):
    """
    Historique des connexions
    Enregistre chaque tentative de connexion
    """
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="login_history",
        null=True,
        blank=True,
        verbose_name="Utilisateur"
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Date/heure de connexion"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="Adresse IP"
    )
    user_agent = models.CharField(
        max_length=500,
        blank=True,
        help_text="User Agent du navigateur"
    )
    success = models.BooleanField(
        default=True,
        db_index=True,
        help_text="Connexion reussie"
    )

    class Meta:
        ordering = ["-timestamp"]
        verbose_name = "Connexion"
        verbose_name_plural = "Journal de connexions"
        indexes = [
            models.Index(fields=["user", "-timestamp"]),
            models.Index(fields=["success", "-timestamp"]),
        ]

    def __str__(self):
        status = "Succes" if self.success else "Echec"
        return f"{self.user.email if self.user else 'Anonyme'} - {status} - {self.timestamp}"