from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy  # Para usar URLs como redirecionamento
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from .utils import verificar_usuario
from .models import Paciente, Usuario, Horario
from django.shortcuts import render, get_object_or_404, redirect
from .models import Psicologo
from django.http import HttpResponse

def register_view(request):
    if request.method == 'POST':
        # Recupera os dados do formulário
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')
        senha = request.POST.get('senha')
        cpf = request.POST.get('cpf')
        data_nascimento = request.POST.get('data_nascimento')
        numero_usp = request.POST.get('numero_usp')

        # Cria um novo paciente
        paciente = Paciente(
            nome=nome,
            email=email,
            telefone=telefone,
            senha=senha,
            cpf=cpf,
            data_nascimento=data_nascimento,
            numero_usp=numero_usp
        )
        # Salva o paciente no banco de dados
        paciente.registrarPaciente(request)

        # Redireciona para a página de login ou dashboard
        return redirect('dashboard')  # Redireciona para a página inicial (login)

    return render(request, 'usuarios/register.html')

""" from django.shortcuts import render
from .forms import BaseUserForm, PsicologoForm, AlunoForm

def register(request):
    if request.method == "POST":
        user_type = request.POST.get("user_type")
        if user_type == "psicologo":
            form = PsicologoForm(request.POST)
        elif user_type == "aluno":
            form = AlunoForm(request.POST)
        else:
            form = BaseUserForm(request.POST)

        if form.is_valid():
            # Processar o formulário (exemplo: salvar no banco de dados)
            return render(request, "usuarios/register_success.html")

    else:
        form = BaseUserForm()

    return render(request, "usuarios/register.html", {"form": form})
 """


# Classe personalizada para o Login
def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario, mensagem = verificar_usuario(email, senha)
        print(f"Usuário autenticado: {usuario}")
        print(f"Mensagem: {mensagem}")
        if usuario: 
            request.session['usuario_id'] = usuario.id
            print("Redirecionando para o dashboard...")
            return redirect('dashboard')
        else:
            print("Erro no login. Retornando para a página de login.")
            return render(request, 'usuarios/login.html', {'erro': mensagem})
    print("Exibindo página de login.")
    return render(request, 'usuarios/login.html')

def dashboard(request):
    usuario_id = request.session.get('usuario_id')

    if not usuario_id:
        # Se não há usuário logado, redirecionar para a página de login
        return redirect('login')  # Use o nome da URL do login

    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')

    # Renderizar a dashboard com informações do usuário
    return render(request, 'usuarios/dashboard.html', {'usuario': usuario})

def configurar_perfil(request):
    
    usuario_id = request.session.get('usuario_id')

    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')


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

def gerenciar_consultas(request):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    paciente = get_object_or_404(Paciente, id=user_id) 
    consultas = []  # Substituir por consultas reais do banco de dados 
    consultas = Horario.objects.filter(paciente=paciente).order_by('data', 'hora_inicio')
    return render(request, 'usuarios/gerenciar_consultas.html', {"consultas": consultas})

def logout_view(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']  # Remove o ID da sessão
    return redirect('home')

def register_view(request):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
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

def marcar_consulta(request):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    if request.method == 'POST':
        return redirect('marcar_consulta')
    # Busca todos os psicólogos 
    psicologos = Psicologo.objects.all()
    return render(request, 'usuarios/marcar_consulta.html', {'psicologos': psicologos})

def listar_horario(request, psicologo_id):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    psicologo = get_object_or_404(Psicologo, id=psicologo_id)
    print(psicologo) 
    horarios_disponiveis = psicologo.horarios.filter(disponivel=True)
    for i in horarios_disponiveis: 
        print(i)
    return render(request, 'usuarios/listar_horario.html', {'psicologo': psicologo, 'horarios': horarios_disponiveis})

def marcar_horario(request, horario_id):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    horario = get_object_or_404(Horario, id=horario_id)
    if horario.disponivel:
        user_id = request.session['usuario_id']
        print(user_id)
        paciente = get_object_or_404(Paciente, id=user_id)
        print(paciente.nome)
        horario.marcar_consulta(paciente)
        return redirect('marcar_consulta')
    else:
        return render(request, 'usuarios/erro.html', {'mensagem': 'Este horário já foi reservado.'})

def perfil_psicologo(request, psicologo_id):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    psicologo = get_object_or_404(Psicologo, id=psicologo_id)
    return render(request, 'perfil_psicologo.html', {'psicologo': psicologo})

def calendario_psicologo(request, psicologo_id):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    psicologo = get_object_or_404(Psicologo, id=psicologo_id)
    horarios = psicologo.horarios.filter(disponivel=True)

    # Obtenha os dias com horários disponíveis
    dias_disponiveis = horarios.values_list('data', flat=True).distinct()

    return render(request, 'calendario_psicologo.html', {
        'psicologo': psicologo,
        'dias_disponiveis': dias_disponiveis,
    })

def horarios_por_dia(request, psicologo_id, data):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    psicologo = get_object_or_404(Psicologo, id=psicologo_id)
    horarios = psicologo.horarios.filter(disponivel=True, data=data)

    return JsonResponse({
        'horarios': [
            {'id': horario.id, 'hora_inicio': horario.hora_inicio, 'hora_fim': horario.hora_fim}
            for horario in horarios
        ]
    })

def confirmar_consulta(request, horario_id):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    horario = get_object_or_404(Horario, id=horario_id, disponivel=True)
    psicologo = horario.psicologo
    paciente = request.user.paciente  # Assumindo que o usuário logado é um paciente

    if request.method == 'POST':
        # Salvar a consulta
        Consulta.objects.create(paciente=paciente, psicologo=psicologo, horario=horario)

        # Marcar o horário como indisponível
        horario.disponivel = False
        horario.save()

        # Redirecionar para o dashboard
        return redirect('dashboard')

    return render(request, 'confirmar_consulta.html', {'horario': horario, 'psicologo': psicologo})


def cadastrar_horarios(request):
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    
    if not hasattr(request.user, 'psicologo'):
        return HttpResponse("Acesso negado.")

    psicologo = request.user.psicologo
    if request.method == "POST":
        data = request.POST.get("data")
        hora_inicio = request.POST.get("hora_inicio")
        hora_fim = request.POST.get("hora_fim")

        Horario.objects.create(
            psicologo=psicologo, data=data, hora_inicio=hora_inicio, hora_fim=hora_fim
        )
        return redirect('dashboard')

    return render(request, 'usuarios/cadastrar_horarios.html')

def horarios_disponiveis(request, psicologo_id):
    
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    
    psicologo = get_object_or_404(Psicologo, id=psicologo_id)
    horarios = Horario.objects.filter(psicologo=psicologo, disponivel=True)

    if request.method == "POST":
        horario_id = request.POST.get("horario_id")
        horario = get_object_or_404(Horario, id=horario_id, disponivel=True)
        horario.marcar_consulta(request.user.paciente)
        return redirect('dashboard')

    return render(request, 'usuarios/horarios_disponiveis.html', {'horarios': horarios, 'psicologo': psicologo})


def vincular_horario(request, horario_id):
    
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    
    if not hasattr(request.user, 'psicologo'):
        return HttpResponse("Acesso negado.")

    horario = get_object_or_404(Horario, id=horario_id, psicologo=request.user.psicologo)

    if request.method == "POST":
        paciente_id = request.POST.get("paciente_id")
        paciente = get_object_or_404(Paciente, id=paciente_id)
        horario.marcar_consulta(paciente)
        return redirect('dashboard')

    return render(request, 'usuarios/vincular_horario.html', {'horario': horario})
