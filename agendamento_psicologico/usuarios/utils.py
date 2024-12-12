from django.contrib.auth.hashers import check_password
from .models import Usuario

def verificar_usuario(email, senha):
    """
    Verifica se o usuário existe e se a senha está correta.

    Args:
        email (str): O email do usuário.
        senha (str): A senha fornecida pelo usuário.

    Returns:
        tuple: (objeto do usuário ou None, mensagem de sucesso ou erro)
    """
    try:
        # Busca o usuário pelo email
        usuario = Usuario.objects.get(email=email)
        
        # Valida a senha
        if check_password(senha, usuario.senha):
            return usuario, "Usuário autenticado com sucesso."
        else:
            return None, "Senha incorreta."
    except Usuario.DoesNotExist:
        return None, "Usuário não encontrado."
