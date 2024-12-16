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


#View para cadastro sem admin -> decidimos por nao utilizar

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


# View de login para pacientes e psicologos
def login_view(request):
    if request.method == "POST":
        
        #salvar email e senha enviados no formulario HTML
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        #buscar no banco de dados e valida senha 
        usuario, mensagem = verificar_usuario(email, senha)
        print(f"Usuário autenticado: {usuario}")
        print(f"Mensagem: {mensagem}")
        
        #verificar se foi bem sucedido
        if usuario: 
            #salvar ID na sessao do navegador -> utilizado para verificar se esta logado
            request.session['usuario_id'] = usuario.id
            print("Redirecionando para o dashboard...")
            return redirect('dashboard')
        else:
            print("Erro no login. Retornando para a página de login.")
            return render(request, 'usuarios/login.html', {'erro': mensagem})
    print("Exibindo página de login.")
    return render(request, 'usuarios/login.html')


#View para render do dashboard
def dashboard(request):
    
    #Verificar se está logado
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


#View para render do perfil e sua modificacao -> acesso ao banco nao implementado
def configurar_perfil(request):
     
    #Verifica se esta logado
    usuario_id = request.session.get('usuario_id')

    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=usuario_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')

    # verifica se request foi do tipo POST
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


# Render da pagina de gerenciar consultas. Renderiza as consultas marcadas do paciente
def gerenciar_consultas(request):
    
    #verificar se esta logado
    user_id = request.session['usuario_id']
    try:
        # Buscar o usuário pelo ID armazenado na sessão
        usuario = Usuario.objects.get(id=user_id)
    except Usuario.DoesNotExist:
        # Se o usuário não existe, redirecionar para o login
        return redirect('login')
    paciente = get_object_or_404(Paciente, id=user_id) 
    consultas = [] 
    consultas = Horario.objects.filter(paciente=paciente).order_by('data', 'hora_inicio')
    return render(request, 'usuarios/gerenciar_consultas.html', {"consultas": consultas})


#Realiza o logout do usuario
def logout_view(request):
    if 'usuario_id' in request.session:
        del request.session['usuario_id']  # Remove o ID da sessão
    return redirect('home')


#Realiza o processamento das consultas
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


#Lista horarios disponiveis do psicologo
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


#associa um horario a um paciente. Ja tem associacao ao psicologo na criacao na visao admin.
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


#renderiza paerfil do psicologo
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


""" Codigo cadastro de horario fora do admin -> decidimos nao utilizar

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
 """
 
 
 #lista horarios cadastrados por psicologos que estao disponiveis
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


""" def vincular_horario(request, horario_id):
    
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
 """