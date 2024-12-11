from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Usuario

class RutUsuuaBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            print(f"RutUsuuaBackend: Buscando usuario con RutUsuua: {username}")
            user = Usuario.objects.get(RutUsuua=username)
            
            if user.check_password(password):
                print("RutUsuuaBackend: Contraseña correcta")
                return user
            else:
                print("RutUsuuaBackend: Contraseña incorrecta")
                return None
                
        except Usuario.DoesNotExist:
            print("RutUsuuaBackend: Usuario no encontrado")
            return None
        except Exception as e:
            print(f"RutUsuuaBackend: Error inesperado: {str(e)}")
            return None

    def get_user(self, user_id):
        try:
            return Usuario.objects.get(pk=user_id)
        except Usuario.DoesNotExist:
            return None