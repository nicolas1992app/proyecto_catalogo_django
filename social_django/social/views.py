from concurrent.futures._base import LOGGER
from datetime import datetime
import json
import pytz
from django.db.transaction import atomic, rollback
from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib import messages
from django.views import View
from django.contrib.auth import logout, authenticate, login
from social.models import Usuarios
from .response import RespuestaJson
from django.contrib.auth.hashers import make_password, check_password


class inicioView(View):
    def get(self, request):
        data_pages = PagesInfo.objects.all()
        info_team = Usuarios.objects.all()
        usuario_data = ""
        if request.user.is_authenticated:
            usuario_data = Usuarios.objects.get(id=request.user.id)
        return render(request, 'base/base.html', {'data': data_pages, 'usuario': usuario_data, 'team': info_team})


class logoutBaseView(View):
    def get(self, request):
        logout(request)
        info_team = Usuarios.objects.all()
        data_pages = PagesInfo.objects.all()
        messages.success(request, 'Hasta pronto')
        return redirect('/')
        #return render(request, 'base/base.html', {'data': data_pages, 'usuario': None, 'team': info_team})


class loginBaseView(View):

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        data_pages = PagesInfo.objects.all()
        info_team = Usuarios.objects.all()

        if user is not None:
            login(request, user)
            usuario_data = Usuarios.objects.get(id=request.user.id)
            messages.success(request, 'Bienvenido :{0} '.format(usuario_data.username))
            return render(request, 'base/base.html', {'data': data_pages, 'usuario': usuario_data, 'team': info_team})
        else:
            messages.error(request, 'Intente de nuevo. ')
            return render(request, 'base/base.html', {'data': data_pages, 'usuario': None})


class RegisterView(View):

    def get(self, request):
        usuarios = Usuarios.objects.all()
        return render(request, 'base/_modal_crear_editar_usuarios.html', {'data': usuarios})

    def post(self, request):
        data_pages = PagesInfo.objects.all()
        usuarios = Usuarios()
        usuariosModel = User()

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
        username = '{}.{}'.format(usuarios.nombre, usuarios.apellido).strip()
        usuariosModel.username = username
        usuariosModel.date_joined = usuarios.ultimo_ingreso
        usuariosModel.first_name = usuarios.nombre
        usuariosModel.last_name = usuarios.apellido
        usuariosModel.last_login = usuarios.ultimo_ingreso
        usuariosModel.is_active = usuarios.estado
        usuariosModel.password = make_password(request.POST.get('password').strip())
        checkpassword = check_password(request.POST['password'], usuariosModel.password)

        if User.objects.filter(username=username).exists():
            info_usuarios = Usuarios.objects.all()
            messages.error(request, 'este nombre de usuario ha sido registrado')
            #return render(request, 'base/base.html', {'data': data_pages, 'usuario': None})
            return RespuestaJson.error("este nombre de usuario ha sido registrado")

        else:
            try:
                with atomic():
                    #usuarios.save()
                    usuariosModel.save()
                    messages.success(request, 'Registro exitoso')
                    return RespuestaJson.exitosa({"catalog_info": "OK"})
            except:
                rollback()
                LOGGER.exception('Falló la creación del registro.')
                messages.success(request, 'Ha ocurrido un error al realizar la acción')
                return RespuestaJson.error('Ha ocurrido un error al realizar la acción')




class RegisterCatalogView(View):

    def get(self, request):
        data_pages = PagesInfo.objects.all()
        return render(request, 'base/_modal_crear_editar_paginas.html', {'data': data_pages})

    def post(self, request):
        paginas = PagesInfo()

        paginas.nombre = request.POST.get('nombre')
        paginas.descripcion = request.POST.get('descripcion')
        paginas.estado_pagina = True
        paginas.enlace = request.POST.get('enlace')
        paginas.fecha_creacion = datetime.now(pytz.utc)
        paginas.ruta_foto = request.FILES.get('imagen', None)
        paginas.editar = True

        if request.is_ajax():

            catalog_info = {
                "nombre": paginas.nombre,
                "descripcion": paginas.descripcion,
                "enlace": paginas.enlace,
                "fecha_creacion": paginas.fecha_creacion,
                "estado_pagina": True,
                "ruta_foto": "portfolio-1.jpg",
            }
            try:
                with atomic():
                    paginas.save()
                    messages.success(request, 'Registro exitoso')
                    return RespuestaJson.exitosa({"catalog_info": catalog_info})
            except:
                rollback()
                LOGGER.exception('Falló la creación del registro.')
                messages.success(request, 'Ha ocurrido un error al realizar la acción')
                return RespuestaJson.error('Ha ocurrido un error al realizar la acción')
        else:
            messages.error(request, 'Ha ocurrido un error al realizar la acción')
            return RespuestaJson.error('Ha ocurrido un error al realizar la acción')


class RegisterCatalogEditarView(View):

    def get(self, request, id):
        data_pages = PagesInfo.objects.get(id=id)
        data_pages.editar = True
        return render(request, 'base/_modal_crear_editar_paginas.html', {'data': data_pages})

    def post(self, request, id):
        paginas = PagesInfo()

        consecutivo_db = PagesInfo.objects.get(id=id)

        paginas.nombre = request.POST.get('nombre')
        paginas.descripcion = request.POST.get('descripcion')
        paginas.estado_pagina = True
        paginas.enlace = request.POST.get('enlace')
        paginas.fecha_creacion = datetime.now(pytz.utc)
        paginas.ruta_foto = request.FILES.get('imagen', None)
        #paginas.ruta_foto = "portfolio-1.jpg"
        paginas.editar = True
        paginas.id = consecutivo_db.id

        if request.is_ajax():
            catalog_info = {
                "nombre": paginas.nombre,
                "descripcion": paginas.descripcion,
                "enlace": paginas.enlace,
                "fecha_creacion": paginas.fecha_creacion,
                "estado_pagina": True,
                "ruta_foto": "portfolio-1.jpg",
                "estado" : "OK"
            }
            try:
                with atomic():
                    paginas.save(update_fields=['nombre', 'descripcion', 'enlace', 'ruta_foto', 'fecha_creacion'])
                    messages.success(request, 'Se ha editado: {0}'.format(paginas.nombre))
                    return RespuestaJson.exitosa({"catalog_info": catalog_info})
            except:
                rollback()
                LOGGER.exception('Falló la edición del registro.')
                messages.error(request, 'Ha ocurrido un error al realizar la acción')
                return RespuestaJson.error('Ha ocurrido un error al realizar la acción')

        else:
            messages.error(request, 'Ha ocurrido un error al realizar la acción')
            return RespuestaJson.error('Ha ocurrido un error al realizar la acción')


class CatalogDeleteView(View):

    def post(self, request, id):
        info_pages = PagesInfo.objects.get(id=id)
        body_unicode = request.body.decode('utf-8')
        datos_registro = json.loads(body_unicode)
        justificacion = datos_registro['justificacion']
        if not info_pages.estado_pagina:
            return RespuestaJson.error("Este registro ya ha sido anulado.")
        try:
            with atomic():
                info_pages.estado_pagina = False
                info_pages.descripcion = justificacion
                info_pages.fecha_creacion = datetime.now(pytz.utc)
                info_pages.save(update_fields=['estado_pagina', 'descripcion', 'fecha_creacion'])
                messages.success(request, 'Registro {0} anulado'.format(info_pages.nombre))
                return RespuestaJson.exitosa()
        except:
            rollback()
            LOGGER.exception('Error anulando el registro')
            return RespuestaJson.error('Ha ocurrido un error al realizar la acción')