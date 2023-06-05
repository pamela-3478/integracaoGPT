from django.http.response import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from asgiref.sync import async_to_sync
import json

from .utils.GptApi import chat_gpt_async

# Create your views here.

def chat_gpt_sync(message, chat_context):
    return async_to_sync(chat_gpt_async)(message, chat_context)

def logout(req):
    if req.method == 'GET':
        return render(req, 'users/registro.html')
    if req.user.is_authenticated:
        logout(req)
    return render(req, 'users/registro.html')
    
def homePage(req): 
    return render(req, 'home/home.html')

def userHome(req): 
    return render(req, 'users/registro.html')
    
def userRegister(req): 
    if req.method == 'GET':
        return render(req, 'users/registro.html')    
    
    # Salva os dados do usuario para o banco de dados
    nome = req.POST.get('nome')
    email = req.POST.get('email')
    senha = req.POST.get('senha')

    # Verifica se o usuario já existe no banco de dados via email
    user = User.objects.filter(email=email)
    if user.exists():
        return HttpResponse('Email já cadastrado')
    
    # Se não existir cria o usuario com os dados enviados
    user = User.objects.create_user(username=nome, email=email, password=senha)
    user.save()
    
    # return render(req, 'users/registro.html')
    return render(req, 'users/registro.html')

def userLogin(req):
    if req.method == 'GET':
        return render(req, 'users/registro.html')

    email = req.POST.get('email')
    password = req.POST.get('senha')

    user = authenticate(req, username=email, password=password)

    if user:
        login(req, user)
        return HttpResponse('AUTENTICADO')
    else:
        return render(req, 'users/registro.html')
    
def chatBot(req):
    if req.method == 'GET':
        return json.dumps({'status': None})

    if 'chat-context' not in req.session or req.session['chat-context'] == None:
        req.session['chat-context'] = {
            'messages': [
                {'role': 'system', 'content': 'Você é um assistente de bate-papo. Para uma de carros que parcela carros em 120 vezes, se o cliente pedir informe sobre o carro as seguintes características: rodas, banco, marca, modelo, ano, motor, velocidade máxima e demais informações'}
            ]
        }

    data = json.loads(req.body.decode())
    chat_context = req.session['chat-context']
    user_message = data['mensagem']

    chat_context['messages'].append({'role': 'user', 'content': user_message})
    response_message = chat_gpt_sync(user_message, chat_context)

    chat_context['messages'].append({'role': 'assistant', 'content': response_message})
    req.session['chat-context'] = chat_context

    return JsonResponse(response_message, safe=False)

def resetarChat(req): 
    req.session['chat-context'] = None
    return HttpResponse('OK')