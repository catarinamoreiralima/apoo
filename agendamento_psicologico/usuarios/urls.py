# urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Página de login personalizada
    path('login.html', views.CustomLoginView.as_view(), name='login'),
    path('register.html', views.register_view, name='register'),
    path('dashboard.html', views.dashboard, name='dashboard'),  # URL do dashboard
    path('configurar_perfil.html', views.configurar_perfil, name='configurar_perfil'),  # URL para configurar perfil
    path('gerenciar_consultas/', views.gerenciar_consultas, name='gerenciar_consultas'),  # URL para gerenciar consultas
    path('marcar_consulta/', views.marcar_consulta, name='marcar_consulta'),  # URL para gerenciar consultas
    path('logout/', views.logout_view, name='logout'),  # URL para logout
    path('password_reset/', 
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
]
