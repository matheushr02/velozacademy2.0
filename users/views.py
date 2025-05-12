from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Perfil

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard:home')
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.is_staff or user.is_superuser:
                return redirect('dashboard:home')
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            messages.error(request, 'As senhas não conferem')
            return render(request, 'users/registro.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Nome de usuário já existe')
            return render(request, 'users/registro.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email já cadastrado')
            return render(request, 'users/registro.html')
            
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        
        # Perfil is created automatically via signal
        
        messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
        return redirect('users:login')
    
    return render(request, 'users/registro.html')

@login_required
def perfil_view(request):
    user = request.user
    
    if request.method == 'POST':
        # Update profile info
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        
        # Update profile
        perfil = user.perfil
        perfil.bio = request.POST.get('bio')
        
        if 'avatar' in request.FILES:
            perfil.avatar = request.FILES['avatar']
            
        perfil.save()
        
        messages.success(request, 'Perfil atualizado com sucesso')
        return redirect('users:perfil')
    
    return render(request, 'users/perfil.html')

def recuperar_senha_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        
        if User.objects.filter(email=email).exists():
            # In a real application, you would send an email with a recovery link
            messages.success(request, 'Enviamos instruções para recuperar sua senha no email informado.')
            return redirect('users:login')
        else:
            messages.error(request, 'Email não encontrado')
    
    return render(request, 'users/recuperar_senha.html')
