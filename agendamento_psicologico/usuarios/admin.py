from django.contrib import admin
from django.contrib import admin
from .models import Psicologo, Paciente, Horario
# Register your models here.

class HorarioInline(admin.TabularInline):  # Ou admin.StackedInline para exibição vertical
    model = Horario
    extra = 1  # Número de horários adicionais exibidos para adicionar

@admin.register(Psicologo)
class PsicologoAdmin(admin.ModelAdmin):
    
    inlines = [HorarioInline] 
    
    list_display = ('nome', 'email', 'telefone', 'registro_profissional', 'abordagem')
    
    def save_model(self, request, obj, form, change):
        if not obj.senha.startswith('pbkdf2_'):  # Evita re-hashear senhas
            obj.set_password(obj.senha)
        super().save_model(request, obj, form, change)
        
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'data_nascimento', 'numero_usp')
    
    def save_model(self, request, obj, form, change):
        if not obj.senha.startswith('pbkdf2_'):  # Evita re-hashear senhas
            obj.set_password(obj.senha)
        super().save_model(request, obj, form, change)
        