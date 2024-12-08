# views.py

from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy  # Para usar URLs como redirecionamento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Classe personalizada para o Login
class CustomLoginView(LoginView):
    template_name = 'usuarios/login.html'  # Definindo o template personalizado

    # Redirecionamento após o login bem-sucedido
    def get_success_url(self):
        return reverse_lazy('dashboard')  # Redireciona para o dashboard após login


@login_required
def dashboard(request):
    """
    View para o dashboard do usuário. 
    Mostra opções como Configurar Perfil, Gerenciar Consultas e Logout.
    """
    return render(request, 'usuarios/dashboard.html')


@login_required
def configurar_perfil(request):
    """
    View para a página de configuração de perfil.
    Implementa lógica para editar os dados do perfil do usuário.
    """
    #user_profile = request.user.profile

    if request.method == 'POST':
        # Atualizar campos do usuário
        user = request.user
        user.username = request.POST.get('nome', user.username)
        user.save()

        # Atualizar campos do perfil
        # user_profile.birthdate = request.POST.get('nascimento', user_profile.birthdate)
        # user_profile.phone = request.POST.get('telefone', user_profile.phone)
        # user_profile.description = request.POST.get('descricao', user_profile.description)

        # Atualizar foto de perfil, se fornecida
        # if 'photo' in request.FILES:
            # user_profile.photo = request.FILES['photo']

        # user_profile.save()

        # messages.success(request, 'As informações foram salvas com sucesso!')
        # return redirect('configurar_perfil')

    return render(request, 'usuarios/configurar_perfil.html')


@login_required
def gerenciar_consultas(request):
    """
    View para gerenciar consultas.
    Pode ser usada para listar, criar ou editar consultas do usuário.
    """
    # Exemplo básico de renderização
    # Você pode passar consultas do banco de dados no contexto, se necessário
    consultas = []  # Substituir por consultas reais do banco de dados
    return render(request, 'usuarios/gerenciar_consultas.html', {"consultas": consultas})


def logout_view(request):
    """
    View para fazer logout do usuário e redirecioná-lo para a página de login.
    """
    logout(request)  # Faz o logout do usuário atual
    return redirect('login')  # Redireciona para a página de login


def register_view(request):
    """
    View para registrar um novo usuário.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Opcional: Logar automaticamente o usuário após o registro
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            messages.success(request, 'Usuário cadastrado com sucesso! Você pode fazer login agora.')
            return redirect('login')
        else:
            messages.error(request, 'Erro ao cadastrar usuário. Por favor, verifique os dados inseridos.')
    else:
        form = UserCreationForm()
    return render(request, 'usuarios/register.html', {'form': form})

@login_required
def marcar_consulta(request):
    if request.method == 'POST':
        return redirect('marcar_consulta.html') 
    return render(request, 'usuarios/marcar_consulta.html')  