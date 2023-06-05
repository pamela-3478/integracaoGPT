from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    # rota, view responsavel, nome de referencia
    path('', views.homePage, name = 'homePage'),
    path('user/', views.userHome, name = 'user_home'),
    path('user/registro', views.userRegister, name = 'registro_usuario'),
    path('user/login', views.userLogin, name = 'login_usuario'),
    path('user/logout', views.logout, name='logout'),
    path('admin', admin.site.urls),

    path('reset-chat', views.resetarChat, name='resetarChat'),
    path('chat/response', views.chatBot, name='chatBot')
]