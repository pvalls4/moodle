from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.conf import settings
import json
# Create your models here.
class Centro(models.Model):
    nombre = models.CharField(max_length=200)
    localitat = models.CharField(max_length=200)
    def __str__(self):
        return self.nombre
class Curso(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=255)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre
    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)
    
class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.pk} - {self.nombre}'

class Tarea(models.Model):
    nombre = models.CharField(max_length=200)
    ponderacion = models.IntegerField(default=0)
    visibilidad = models.BooleanField(default=False)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

class VRTarea(models.Model):
    nombre = models.CharField(max_length=200)
    exercise = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    ponderacion = models.IntegerField(default=0)
    visibilidad = models.BooleanField(default=False)
    minversion = models.CharField(max_length=255, null=True, blank=True)
    autograde = models.CharField(max_length=255, null=True, blank=True)
    version = models.CharField(max_length=255, null=True, blank=True)
    performance_data = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.nombre
 
class NivelPrivacidad(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.CharField(max_length=255)
    def __str__(self):
        return self.nombre
        
class User(AbstractUser):
    correo = models.EmailField(max_length=254, unique = True)
    centro = models.ForeignKey(Centro, on_delete=models.CASCADE, null=True, blank=True)
    privacidad = models.ForeignKey(NivelPrivacidad, on_delete=models.CASCADE, null=True, blank=True)

    REQUIRED_FIELDS = ['first_name', 'last_name']
    def __str__(self):
        return "{}".format(self.username)

class Entrega(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, null=True, blank=True)
    vrtarea = models.ForeignKey(VRTarea, on_delete=models.CASCADE, null=True, blank=True)
    archivo = models.FileField(upload_to="./archivos/entregas/",blank=True)
    fecha_entrega = models.DateTimeField()
    pin = models.IntegerField(null=True, blank=True)

    def __str__(self):
        try:
            resul = self.tarea.nombre
        except: 
            resul = self.pin    
        return str(resul)
      
class Suscripcion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=200)
    def __str__(self):
        return self.tipo

class Recurso(models.Model):
    titulo = models.CharField(max_length=200)
    texto = models.CharField(max_length=255, blank=True)
    archivo = models.FileField(upload_to="./archivos/recursos/", blank=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)                                            
    def __str__(self):
        return self.titulo

class Calificacion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tarea = models.ForeignKey(Tarea, on_delete=models.CASCADE, null=True, blank=True)
    vrtarea = models.ForeignKey(VRTarea, on_delete=models.CASCADE, null=True, blank=True)
    nota = models.IntegerField(null=True)
    fecha_entrega = models.DateTimeField()
    comentario_profesor = models.CharField(max_length=255, null=True, blank=True)
    comentario_alumno = models.CharField(max_length=255, null=True, blank=True)
    def str(self):
        return '{}{}'.format(self.nota, self.user)

class VRCalificacion(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vrtarea = models.ForeignKey(VRTarea, on_delete=models.CASCADE)
    nota = models.IntegerField(null=True)
    fecha_entrega = models.DateTimeField()
    comentario_profesor = models.CharField(max_length=255, null=True, blank=True)
    comentario_alumno = models.CharField(max_length=255, null=True, blank=True)
    def str(self):
        return '{}{}'.format(self.nota, self.user)


