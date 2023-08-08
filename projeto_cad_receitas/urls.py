from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from app_cad_receitas import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('criar_receitas', views.criar_receitas, name='criar_receitas'),
    path('ver_cardapio', views.ver_cardapio, name='ver_cardapio'),
    path('cadastrar_receita', views.cadastrar_receita, name='cadastrar_receita'),
    path('calcular_lucro', views.calcular_lucro, name='calcular_lucro'),
    path('excluir_receita/<int:id_receita>/', views.excluir_receita, name='excluir_receita'),
    path('editar_receita/<int:receita_id>/', views.editar_receita, name='editar_receita'),
    path('editar_ingrediente/<int:id_ingrediente>/', views.editar_ingrediente, name='editar_ingrediente'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
]
