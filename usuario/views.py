from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

def login_view(request):
    if request.method == 'POST':
        RutUsuua = request.POST.get('RutUsuua')
        password = request.POST.get('password')
        
        print(f"Intentando login con RutUsuua: {RutUsuua}")
        
        user = authenticate(request, username=RutUsuua, password=password)
        if user is not None:
            login(request, user)
            return redirect('inventario:base')
        error_message = 'RUT o contraseña inválidos.'
    else:
        error_message = ''
    return render(request, 'usuario/login.html', {'error_message': error_message})

def logout_view(request):
    print("Cerrando sesión")
    logout(request)
    return redirect('usuario:login')