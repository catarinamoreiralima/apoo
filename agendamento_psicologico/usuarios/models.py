from django.db import models
from distutils.archive_util import make_zipfile
from xml.parsers.expat import model
from django.forms import CharField, Field
from django.utils import timezone
import datetime
from enum import Enum
from django.contrib.auth.hashers import make_password

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=15)
    senha = models.CharField(max_length=128)  # Alterado para suportar senhas hasheadas
    cpf = models.CharField(max_length=15)

    def save(self, *args, **kwargs):
        if not self.senha.startswith('pbkdf2_'):  # Evita re-hashear senhas
            self.senha = make_password(self.senha)
        super().save(*args, **kwargs)

    def set_password(self, raw_password):
        self.senha = make_password(raw_password)
        self.save()
        
class Paciente (Usuario):
    data_nascimento = models.DateField()
    numero_usp = models.CharField(max_length=10)
    
class Psicologo(Usuario):
    registro_profissional = models.CharField(max_length=100)
    abordagem = models.CharField(max_length=100)

class Administrador (Usuario):
    cargo = models.CharField(max_length=100) 


    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

class Hora(Enum):
    @classmethod
    def choices(cls):
        return [(f'{hora:02}h00', f'{hora}:00') for hora in range(24)]

class Horario(models.Model):
    psicologo = models.ForeignKey(
        Psicologo, on_delete=models.CASCADE, related_name="horarios"
    )
    data = models.DateField()
    hora_inicio = models.CharField(
        max_length=20,
        choices=Hora.choices(),
    )
    hora_fim = models.CharField(
        max_length=20,
        choices=Hora.choices(),
    )
    disponivel = models.BooleanField(default=True)
    paciente = models.ForeignKey(
        Paciente, null=True, blank=True, on_delete=models.SET_NULL, related_name="horarios"
    )
    
    def marcar_consulta(self, paciente):
        if self.disponivel:
            self.paciente = paciente
            self.disponivel = False
            self.save()
        else:
            raise ValueError("Horário já reservado.")
