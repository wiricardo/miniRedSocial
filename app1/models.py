from django.db import models
from django.contrib.auth.models import User


# -----------------------------
# PERFIL DE USUARIO
# -----------------------------
class datosUsuario(models.Model):
    profesion = models.CharField(max_length=48, null=True, blank=True)
    nroCelular = models.CharField(max_length=16, null=True, blank=True)
    perfilUsuario = models.CharField(max_length=256, null=True, blank=True)
    usrRel = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    fotoPerfil = models.ImageField(upload_to='avatars/', null=True, blank=True)

    def __str__(self):
        return self.usrRel.username if self.usrRel else "Sin usuario"


# -----------------------------
# PUBLICACIONES (POSTS)
# -----------------------------
class publicacion(models.Model):
    titulo = models.CharField(max_length=64, null=True, blank=True)
    descripcion = models.TextField(null=True, blank=True)
    autorPub = models.ForeignKey(User, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='publicaciones/', null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo or 'Publicación sin título'} - {self.autorPub.username}"


# -----------------------------
# COMENTARIOS
# -----------------------------
class comentario(models.Model):
    descripcion = models.TextField(null=True, blank=True)
    pubRel = models.ForeignKey(publicacion, on_delete=models.CASCADE, related_name='comentarios')
    autoCom = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    respuesta_a = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='respuestas'
    )

    def __str__(self):
        return f"Comentario de {self.autoCom.username} en {self.pubRel.titulo or 'Publicación'}"

class mensaje(models.Model):
    emisor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_enviados')
    receptor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensajes_recibidos')
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.emisor.username} -> {self.receptor.username}: {self.contenido}"