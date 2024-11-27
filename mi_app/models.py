from django.db import models
from django.contrib.auth.models import User

class Autor(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    titulo = models.CharField(max_length=100)
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    editorial = models.CharField(max_length=100, default="Desconocida")
    anio = models.PositiveIntegerField(default=0) 
    isbn = models.CharField(max_length=13, unique=True, default="---")

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    id = models.AutoField(primary_key=True) 
    libro = models.ForeignKey('Libro', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE) 
    comentario = models.CharField(max_length=10000)

    def __str__(self):
        return f"Comentario de {self.usuario.username} sobre {self.libro.titulo}"
