from django.db import models
from distutils.archive_util import make_zipfile
from xml.parsers.expat import model
from django.forms import CharField, Field
from django.utils import timezone
import datetime
from enum import Enum

# Create your models here.
class Usuario(models.Model):
    nome = models.Charfield(max_length=100)
    email = models.EmailField(max_length=254)
    telefone = models.CharField(max_length=15)
    senha = models.CharField(max_length=20)
    cpf = models.CharField(max_length=15)
    
    def registrarUsuario(self):
        self.save()
        





class Paciente (Usuario):
    data_nascimento = models.DateField()
    numero_usp = models.CharField(max_length=10)
    
    
    
class Psicologo (Usuario):
    registro_profissional = models.CharField(max_length=100)
    abordagem = models.CharField(max_length=100)
    

class Administrador (Usuario):
    cargo = models.CharField(max_length=100)
    
    

class DiasDaSemana(Enum):
    SEGUNDA = "Segunda-feira"
    TERCA = "Terça-feira"
    QUARTA = "Quarta-feira"
    QUINTA = "Quinta-feira"
    SEXTA = "Sexta-feira"
    SABADO = "Sábado"
    DOMINGO = "Domingo"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]
    
class Mes(Enum):
    JANEIRO = "Janeiro"
    FEVEREIRO = "Fevereiro"
    MARCO = "Março"
    ABRIL = "Abril"
    MAIO = "Maio"
    JUNHO = "Junho"
    JULHO = "Julho"
    AGOSTO = "Agosto"
    SETEMBRO = "Setembro"
    OUTUBRO = "Outubro"
    NOVEMBRO = "Novembro"
    DEZEMBRO = "Dezembro"

    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]

class Hora(Enum):
    H00_00 = "0h00"
    @classmethod
    def choices(cls):
        return [(key.name, key.value) for key in cls]    
    
    
class Horario(models.Model):
    dia_da_semana = models.CharField(
        max_length=20,
        choices=DiasDaSemana.choices(),
        default=DiasDaSemana.SEGUNDA.name,
    )
    data = models.DateField()
    
    
    mes = models.CharField(
        max_length=20,
        choices=Mes.choices(),
        default=Mes.JANEIRO.name,
    )
    
    hora_inicio = models.CharField(
        max_length=20,
        choices=Hora.choices(),
        default=Hora.H00_00.name,
    )
    
    hora_fim = models.CharField(
        max_length=20,
        choices=Hora.choices(),
        default=Hora.H00_00.name,
    )
    
    disponivel = True
    
    def registrarHorario(self):
        self.save()


class Consulta(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    psicologo = models.ForeignKey(Psicologo, on_delete=models.CASCADE, related_name="consultas")
    horario = models.OneToOneField(Horario, on_delete=models.CASCADE, related_name="consulta")
