from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Perfil
from .forms import RegistrationForm

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def registro_view(request):
    if request.user.is_authenticated:
        return redirect('core:home')
        
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            
            try:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.first_name = first_name
                user.last_name = last_name
                user.save()
                
                messages.success(request, 'Sua conta foi criada com sucesso! Faça login.')
                
                return redirect('users:login')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao criar sua conta: {e}')
        else:
            messages.error(request, 'Por favor, corrija os erros.')
            
    else:
        form = RegistrationForm()
    return render(request, 'users/registro.html', {'form': form})

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

@login_required
def upgrade_account_view(request):
    if request.method == 'POST':
        #Todo colocar pagamento aqui (api de pagamento)
        #? simula pagamento com sucesso

        perfil = request.user.perfil
        perfil.tipo_usuario = 'estudante'
        perfil.data_assinatura = timezone.now().date()
        perfil.save()
        
        messages.success(request, 'Parabéns! Agora você é um VelozEstudante com acesso completo aos cursos, certificados e mais. Aproveite!')
        return redirect('users:perfil')
    return render(request, 'users/upgrade_account.html')

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
