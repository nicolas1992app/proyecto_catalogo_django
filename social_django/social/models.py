from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='batman.png')

    def __str__(self):
        return f'Perfil de {self.user.username}'

    def following(self):
        user_ids = Relationship.objects.filter(from_user=self.user) \
            .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)

    def followers(self):
        user_ids = Relationship.objects.filter(to_user=self.user) \
            .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    timestamp = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.user.username}: {self.content}'


class Relationship(models.Model):
    from_user = models.ForeignKey(User, related_name='relationships', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='related_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user}'

    class Meta:
        indexes = [
            models.Index(fields=['from_user', 'to_user', ]),
        ]

class PagesInfo(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    estado = models.BooleanField(max_length=5, verbose_name='Estado', null=False, blank=False)
    ruta_foto = models.ImageField(upload_to='fotos-paginas', verbose_name='Foto', null=False, blank=False)
    enlace = models.CharField(max_length=100, verbose_name='Enlace', null=True, blank=True)
    descripcion = models.CharField(max_length=500, verbose_name='Descripcion', null=True, blank=True)
    fecha_creacion = models.DateField(verbose_name='Fecha Creacion', null=False, blank=False)

    def __str__(self):
        return self.enlace

    class Meta:
        verbose_name = 'Pagina'
        verbose_name_plural = 'Paginas'

class Usuarios(models.Model):
    nombre = models.CharField(max_length=100, verbose_name='Nombre', null=False, blank=False)
    apellido = models.CharField(max_length=100, verbose_name='Apelido', null=False, blank=False)
    ruta_foto = models.ImageField(upload_to='fotos-perfil', verbose_name='Foto', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación', null=False, blank=False)
    email = models.CharField(max_length=200, verbose_name='Email', null=False, blank=False)
    telefono = models.CharField(max_length=200, verbose_name='Telefono', null=True, blank=True)
    direccion = models.CharField(max_length=200, verbose_name='Direccion', null=True, blank=True)
    observaciones = models.CharField(max_length=200, verbose_name='Observaciones', null=True, blank=True)
    cargo = models.CharField(max_length=200, verbose_name='Observaciones', null=True, blank=True)
    usuario = models.OneToOneField(User, on_delete=models.DO_NOTHING, verbose_name='Usuario', null=True, blank=True,
                                related_name='usuario')


    def __str__(self):
        return self.usuario

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

#user = User.objects.last()
#print(user.id)
#usuarios = Usuarios.objects.create(nombre='', apellido='',ruta_foto='',fecha_creacion='',email='',telefono='',observaciones='')
