from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from django.db import transaction, IntegrityError
from .models import Perfil
from .forms import RegistrationForm, UserUpdateForm, PerfilUpdateForm
import logging

logger = logging.getLogger(__name__)

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():    
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {username}!')
                next_url = request.POST.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('home')
            else:
                messages.error(request, 'Nome de usuário ou senha inválidos.')
        else:
            messages.error(request, 'Por favor, corrija os erros.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form, 'next': request.GET.get('next', '')})

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
                with transaction.atomic():
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()
                
                messages.success(request, 'Sua conta foi criada com sucesso! Faça login.')
                
                return redirect('users:login')
            except IntegrityError as e:
                logger.error(f"IntegrityError during registration for {username}/{email}: {e}")
                messages.error(request, 'Ocorreu um erro inesperado ao salvar seus dados. Nome de usuário ou email podem já existir.')
            except Exception as e:
                logger.error(f"Unexpected error during registration for {username}/{email}: {e}")
                messages.error(request, f'Ocorreu um erro ao criar sua conta. Tente outra vez. Detalhes: {e}')
        else:
            messages.error(request, 'Por favor, corrija os erros.')
    else:
        form = RegistrationForm()
    return render(request, 'users/registro.html', {'form': form})

@login_required
def perfil_view(request):
    user_instance = request.user
    perfil_instance = user_instance.perfil
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user_instance)
        perfil_form = PerfilUpdateForm(request.POST, request.FILES, instance=perfil_instance)
        
        if user_form.is_valid() and perfil_form.is_valid():
        # Update profile info
            user_form.save()
            perfil_form.save()
            messages.success(request, 'Perfil atualizado')
            return redirect('users:perfil')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
       user_form = UserUpdateForm(instance=user_instance)
       perfil_form = PerfilUpdateForm(instance=perfil_instance)
    
    context = {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'user': user_instance
    }
    return render(request, 'users/perfil.html', context)

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
