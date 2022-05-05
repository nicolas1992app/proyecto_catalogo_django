from datetime import datetime

import pytz
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from .forms import UserRegisterForm, PostForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views import View
from django.contrib.auth import logout, authenticate, login
from social.models import Usuarios


class inicioView(View):
    def get(self, request):
        data_pages = PagesInfo.objects.all()
        info_team = Usuarios.objects.all()
        usuario_data = ""
        if request.user.is_authenticated:
            usuario_data = Usuarios.objects.get(usuario_id=request.user.id)
        return render(request, 'base/base.html', {'data': data_pages, 'usuario': usuario_data, 'team': info_team})


class logoutBaseView(View):
    def get(self, request):
        logout(request)
        data_pages = PagesInfo.objects.all()
        return render(request, 'base/base.html', {'data': data_pages, 'usuario': None})


class loginBaseView(View):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        data_pages = PagesInfo.objects.all()
        if user is not None:
            login(request, user)
            usuario_data = Usuarios.objects.get(usuario_id=request.user.id)
            messages.success(request, 'Login exitoso {0}'.format(usuario_data.usuario))
            return render(request, 'base/base.html', {'data': data_pages, 'usuario': usuario_data})
        else:
            messages.error(request, 'Intente de nuevo. ')
            return render(request, 'base/base.html', {'data': data_pages, 'usuario': None})


class RegisterView(View):

    def post(self, request):
        data_pages = PagesInfo.objects.all()
        usuarios = Usuarios()

        usuarios.nombre = request.POST.get('nombre')
        usuarios.apellido = request.POST.get('apellido')
        usuarios.descripcion = request.POST.get('descripcion')
        usuarios.estado = True
        usuarios.ruta_foto = request.FILES.get('foto', None)
        usuarios.cargo = request.POST.get('cargo')
        usuarios.email = request.POST.get('email')
        usuarios.direccion = request.POST.get('direccion')
        usuarios.telefono = request.POST.get('telefono')
        usuarios.ultimo_ingreso = datetime.now(pytz.utc)

        usuarios.save()
        messages.success(request, 'Registro exitoso')
        return render(request, 'base/base.html', {'data': data_pages, 'usuario': usuarios})


def inicio(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'base/templates/sections/catalogo.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('inicio')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'base/templates/sections/register.html', context)


@login_required
def post(request):
    current_user = get_object_or_404(User, pk=request.user.pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = current_user
            post.save()
            messages.success(request, 'Post enviado')
            return redirect('inicio')
    else:
        form = PostForm()
    return render(request, 'base/post.html', {'form': form})


def profile(request, username=None):
    current_user = request.user
    if username and username != current_user.username:
        user = User.objects.get(username=username)
        posts = user.posts.all()
    else:
        posts = current_user.posts.all()
        user = current_user
    return render(request, 'base/profile.html', {'user': user, 'posts': posts})


def follow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = Relationship(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'sigues a {username}')
    return redirect('inicio')


def unfollow(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'Ya no sigues a {username}')
    return redirect('inicio')
