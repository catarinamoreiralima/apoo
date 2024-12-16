from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


#URLs e views associadas
urlpatterns = [
    path("", views.login_view, name='home'), #login 
    path('register/', views.register_view, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),  # URL do dashboard
    path('configurar_perfil.html', views.configurar_perfil, name='configurar_perfil'),  # URL para configurar perfil
    path('gerenciar_consultas.html', views.gerenciar_consultas, name='gerenciar_consultas'),  # URL para gerenciar consultas
    path('marcar_consulta/', views.marcar_consulta, name='marcar_consulta'),  # URL para gerenciar consultas
    path('logout.html', views.logout_view, name='logout'),  # URL para logout
    path('password_reset.html', 
         auth_views.PasswordResetView.as_view(template_name='usuarios/password_reset.html'), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='usuarios/password_reset_done.html'), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='usuarios/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='usuarios/password_reset_complete.html'), 
         name='password_reset_complete'),
    path('marcar_consulta.html', views.marcar_consulta, name='marcar_consulta'),
    path('psicologos/<int:psicologo_id>/', views.perfil_psicologo, name='perfil_psicologo'),
    path('psicologo/<int:psicologo_id>/horarios/', views.listar_horario, name='calendario_psicologo'),
    path('horario/<int:horario_id>/marcar/', views.marcar_horario, name='marcar_horario'),
 
]
