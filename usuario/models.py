from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class UsuarioManager(BaseUserManager):
    def create_user(self, RutUsuua, password, Nombre, ApePa, Telefono, **extra_fields):
        if not RutUsuua:
            raise ValueError('El RutUsuua debe ser proporcionado')
        
        user = self.model(
            RutUsuua=RutUsuua,
            Nombre=Nombre,
            ApePa=ApePa,
            Telefono=Telefono,
            **extra_fields
        )
        user.set_password(password)  # Cifra la contraseña
        user.save(using=self._db)
        return user

    def create_superuser(self, RutUsuua, password, Nombre, ApePa, Telefono, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(
            RutUsuua=RutUsuua,
            password=password,
            Nombre=Nombre,
            ApePa=ApePa,
            Telefono=Telefono,
            **extra_fields
        )

class Usuario(AbstractBaseUser, PermissionsMixin):
    RutUsuua = models.CharField(max_length=100, unique=True)
    Nombre = models.CharField(max_length=100)
    ApePa = models.CharField(max_length=100)
    Telefono = models.CharField(max_length=20)
    
    # Campos adicionales de autenticación estándar
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UsuarioManager()

    USERNAME_FIELD = 'RutUsuua'
    REQUIRED_FIELDS = ['Nombre', 'ApePa', 'Telefono']

    def __str__(self):
        return self.Nombre

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'