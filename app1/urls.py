from django.urls import path
from . import views

app_name = 'app1'

urlpatterns = [
    path('', views.ingresoUsuario, name='ingresoUsuario'),
    path('registro/', views.registroUsuario, name='registroUsuario'),
    path('logout/', views.cerrarSesion, name='cerrarSesion'),
    path('informacion/', views.informacionUsuario, name='informacionUsuario'),
    path('crearPublicacion/',views.crearPublicacion, name='crearPublicacion'),
    path('eliminarPublicacion/<int:idPub>/',views.eliminarPublicacion,name='eliminarPublicacion'),
    path('feed',views.feedPublicaciones,name='feedPublicaciones'),
    path('devolverPublicacion/',views.devolverPublicacion,name='devolverPublicacion'),
    path('publicarComentario/',views.publicarComentario,name='publicarComentario'),
    path('chat/',views.chat,name='chat'),
    path('api/usuarios/',views.listar_usuarios,name='listar_usuarios'),
    path('api/conversacion/<int:idUser>/',views.obtener_conversacion,name='obtener_conversacion'),
    path('api/enviar/<int:idUsuario>/',views.recibirMensaje,name='recibirMensaje'),
    path('api/exportarChat/<int:idUsuario>/', views.exportarChat, name='exportarChat'),
    
    # RUTA PARA PUBLICAR RESPUESTAS A COMENTARIOS
    path('publicarRespuestaComentario/', views.publicarRespuestaComentario, name='publicarRespuestaComentario')
]