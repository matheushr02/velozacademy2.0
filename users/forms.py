from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    first_name = forms.CharField(
        label='Nome',
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary',
                                      'placeholder': 'Seu nome'})
    )

    last_name = forms.CharField(
        label='Sobrenome',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary',
                                      'placeholder': 'Seu sobrenome'})
        )
    
    username = forms.CharField(
        label='Nome de usuário',
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control bg-dark text-light border-secondary',
                                      'placeholder': 'Escolha um nome de usuário'})
    )

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-light border-secondary',
                                       'placeholder': 'Seu email: seuemail@exemplo.com'})
    )
    
    password = forms.CharField(
        label='Senha',
        required=True,
        min_length=7,
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'Crie uma senha forte'})
    )
    
    password2 = forms.CharField(
        label='Confirmar Senha',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'placeholder': 'Coloque sua senha novamente aqui'})
    )
    
    termos = forms.BooleanField(
        label ='Concordo com os <a href="#" class="text-primary">termos e condições</a>',
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'forms-check-input'})
    )
    
    def clean_username(self):
        username =self.cleaned_data.get('username')
        if ' ' in username:
            raise forms.ValidationError('O nome de usuário não pode conter espaços.')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"Nome de usuário '{username}' já está cadastrado. Troque o nome de usuário por outro.")
        return username
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"'{email}' Este email já é cadastrado, use outro porfavor")
        return email
    
    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password != password2:
            raise forms.ValidationError('As duas senhas não são iguais, tente novamente')
        return password2
    

    