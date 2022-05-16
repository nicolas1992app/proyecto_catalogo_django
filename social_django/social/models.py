from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class PagesInfo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    estado_pagina = models.BooleanField(max_length=5, verbose_name='Estado', null=False, blank=False)
    ruta_foto = models.ImageField(upload_to='fotos-paginas', verbose_name='Foto', null=False, blank=False)
    enlace = models.CharField(max_length=100, verbose_name='Enlace', null=True, blank=True)
    descripcion = models.CharField(max_length=500, verbose_name='Descripcion', null=True, blank=True)
    fecha_creacion = models.DateField(verbose_name='Fecha Creacion', null=False, blank=False)

    def __str__(self):
        return self.enlace

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Paginas'

class Usuarios(AbstractBaseUser):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    apellido = models.CharField(max_length=100, verbose_name='Apelido', null=False, blank=False)
    ruta_foto = models.ImageField(upload_to='fotos-perfil', verbose_name='Foto', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación', null=False, blank=False)
    email = models.CharField(max_length=200, verbose_name='Email', null=False, blank=False)
    telefono = models.CharField(max_length=200, verbose_name='Telefono', null=True, blank=True)
    direccion = models.CharField(max_length=200, verbose_name='Direccion', null=True, blank=True)
    observaciones = models.CharField(max_length=200, verbose_name='Observaciones', null=True, blank=True)
    cargo = models.CharField(max_length=200, verbose_name='Observaciones', null=True, blank=True)
    username = models.CharField('Nombre usuario', unique=True, max_length=100)

    USERNAME_FIELD ='useranme'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido']

    def __str__(self):
        return f'{self.nombre}{self.apellido}'


#user = User.objects.last()
#print(user.id)
#usuarios = Usuarios.objects.create(nombre='', apellido='',ruta_foto='',fecha_creacion='',email='',telefono='',observaciones='')
