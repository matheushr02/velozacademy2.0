from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Perfil

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
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        termos = request.POST.get('termos')
        
        if not termos:
            messages.error(request, 'Você precisa aceitar os termos de uso')
            return render(request, 'users/registro.html')
        
        if not all([first_name, username, email, password, password2]):
            messages.error(request, 'Preencha os campos faltantes com *')
            return render(request, 'users/registro.html')
        
        if ' ' in username:
            messages.error(request, 'Nome de usuário não pode conter espaços')
            return render(request, 'users/registro.html')
        
        if password != password2:
            messages.error(request, 'As senhas não são iguais')
            return render(request, 'users/registro.html')
        
        if len(password) < 8:
            messages.error(request, 'A senha tem que conter 8 caracteres no minimo')
            return render(request, 'users/registro.html')
            
        if User.objects.filter(username=username).exists():
            messages.error(request, f"Nome de usuário '{username}' já está cadastrado. Troque o nome por outro")
            return render(request, 'users/registro.html')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, f"'{email}' Email já cadastrado, troque o email por outro")
            return render(request, 'users/registro.html')
            
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            
            #? Cria perfil (automaticamente perfil visitante)
            Perfil.objects.create(user=user)
            
            login(request, user)
            messages.success(request, f'Conta criada! Bem-Vindo(a) {user.first_name}!')            
        except Exception as e:
            messages.error(request, f'Ocorreu um erro ao criar sua conta: {e}')
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
