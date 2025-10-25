from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, FileResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import datosUsuario, publicacion, comentario, mensaje
from django.shortcuts import get_object_or_404
import json
from django.db.models import Q

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter


def ingresoUsuario(request):
    if request.method == 'POST':
        nombreUsuario = request.POST.get('nombreUsuario')
        contraUsuario = request.POST.get('contraUsuario')
        usrObj = authenticate(request, username=nombreUsuario, password=contraUsuario)
        if usrObj is not None:
            login(request, usrObj)
            return HttpResponseRedirect(reverse('app1:informacionUsuario'))
        else:
            return HttpResponseRedirect(reverse('app1:ingresoUsuario'))
    return render(request, 'ingresoUsuario.html')


def registroUsuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        profesion = request.POST.get('profesion')
        celular = request.POST.get('nroCelular')
        perfil = request.POST.get('perfilUsuario')
        foto = request.FILES.get('fotoPerfil')

        # Crear usuario base
        nuevo_usr = User.objects.create_user(
            username=username,
            password=password,
            first_name=nombre,
            last_name=apellido,
            email=email
        )

        # Crear perfil asociado
        datosUsuario.objects.create(
            usrRel=nuevo_usr,
            profesion=profesion,
            nroCelular=celular,
            perfilUsuario=perfil,
            fotoPerfil=foto
        )

        return HttpResponseRedirect(reverse('app1:ingresoUsuario'))

    return render(request, 'registroUsuario.html')

@login_required(login_url='/')
def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('app1:ingresoUsuario'))


@login_required(login_url='/')
def informacionUsuario(request):
    user = request.user

    try:
        perfil = datosUsuario.objects.get(usrRel=user)
    except datosUsuario.DoesNotExist:
        perfil = None

    publicaciones = publicacion.objects.filter(autorPub=user).order_by('-id')

    return render(request, 'informacionUsuario.html', {
        'perfil': perfil,
        'publicaciones': publicaciones
    })

@login_required(login_url='/')
def crearPublicacion(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        imagen = request.FILES.get('imagen')

        publicacion.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            imagen=imagen,
            autorPub=request.user
        )
    return HttpResponseRedirect(reverse('app1:informacionUsuario'))

@login_required(login_url='/')
def eliminarPublicacion(request, idPub):
    pub = publicacion.objects.get(id=idPub)
    if request.method == 'POST':
        pub.delete()
        return HttpResponseRedirect(reverse('app1:informacionUsuario'))
    return HttpResponseRedirect(reverse('app1:informacionUsuario'))

@login_required(login_url='/')
def feedPublicaciones(request):
    publicaciones = publicacion.objects.all().order_by('-fecha_creacion')
    data_feed = []
    for pub in publicaciones:
        try:
            perfil = datosUsuario.objects.get(usrRel=pub.autorPub)
        except datosUsuario.DoesNotExist:
            perfil = None
        data_feed.append({
            'pub':pub,
            'perfil':perfil
        })
    return render(request,'feedPublicaciones.html',{
        'data_feed': data_feed
    })


def devolverPublicacion(request):
    idPub = request.GET.get('idPub')
    try:
        objPub = publicacion.objects.get(id=idPub)
        imagen_url = objPub.imagen.url
        comentariosPub = comentario.objects.filter(pubRel=objPub, respuesta_a=None).order_by('fecha_creacion')
        datosComentario = []
        for comentarioInfo in comentariosPub:
            lista_respuestas = []
            # PREGUNTA 2 - CARGAR LAS RESPUESTAS A LOS COMENTARIOS
            # SECCION DEL EXAMEN FINAL PARA AGREGAR LAS RESPUESTAS:

            
            #CREAR EL OBJETO respuestas QUE CONTIENE LOS COMENTARIOS QUE TIENEN EL ATRIBUTO respuesta_a CON 
            respuestas = comentario.objects.filter(respuesta_a=comentarioInfo).order_by('fecha_creacion')

            #EL VALOR DEL OBJETO comentarioInfo
            #ITERA EN TODAS LAS RESPUESTAS PARA PODER ANEXAR LA INFORMACION EN LA LISTA lista_respuestas
            #LOS DATOS A ANEXAR SON EL AUTOR, LA DESCRIPCION O CONTENIDO, EL ID DE LA RESPUESTA Y LA FECHA
            for resp in respuestas:
                lista_respuestas.append({
                    'autor': f"{resp.autoCom.first_name} {resp.autoCom.last_name}",
                    'descripcion': resp.descripcion,
                    'id': resp.id,
                    'fecha': resp.fecha_creacion.strftime("%d/%m/%Y %H:%M")
                })
            
            # FIN SECCION DE AGREGAR LAS RESPUESTAS


            datosComentario.append({
                'autor': f"{comentarioInfo.autoCom.first_name} {comentarioInfo.autoCom.last_name}",
                'descripcion': comentarioInfo.descripcion,
                'id': comentarioInfo.id,

                # NUEVOS VALORES ENVIADOS:
                'fecha': comentarioInfo.fecha_creacion.strftime("%d/%m/%Y %H:%M"),
                'respuestas': lista_respuestas
                # FIN NUEVOS VALORES
            })
        return JsonResponse({
            'titulo':objPub.titulo,
            'autor':f"{objPub.autorPub.first_name} {objPub.autorPub.last_name}",
            'descripcion': objPub.descripcion,
            'imagen': imagen_url,
            'datosComentario': datosComentario
        })


    except publicacion.DoesNotExist:
        return JsonResponse({'error':'Publicacion no encontrada'})

def publicarComentario(request):
    if request.method == 'POST':
        datosComentario = json.loads(request.body.decode('utf-8'))

        comentarioTexto = datosComentario.get('comentario')
        idPublicacion = datosComentario.get('idPublicacion')

        objPublicacion = publicacion.objects.get(id=idPublicacion)

        comentario.objects.create(
            descripcion=comentarioTexto,
            pubRel = objPublicacion,
            autoCom = request.user,
            respuesta_a = None
        )

        return JsonResponse({'resp':'ok'})
    return JsonResponse({'error':'metodo no permitido'})

def chat(request):
    return render(request, 'chatUsuarios.html')

def listar_usuarios(request):
    allUsers = User.objects.exclude(id=request.user.id)
    data = []
    for usr in allUsers:
        data.append({"id":usr.id, "username":usr.username})
    return JsonResponse(data, safe=False)

def obtener_conversacion(request,idUser):
    actual = request.user
    otro = User.objects.get(id=idUser)

    mensajes = mensaje.objects.filter(
        (Q(emisor=actual, receptor=otro))|(Q(emisor=otro, receptor=actual))
    ).order_by('fecha')

    data = []

    for msgInfo in mensajes:
        data.append({
            "emisor": msgInfo.emisor.username,
            "receptor": msgInfo.receptor.username,
            "contenido": msgInfo.contenido,
            "fecha": msgInfo.fecha.strftime("%H:%M:%S")
        })

    return JsonResponse(data,safe=False)

@csrf_exempt
def recibirMensaje(request,idUsuario):
    if request.method == 'POST':
        data = json.loads(request.body)
        actual = request.user
        receptor = User.objects.get(id=idUsuario)
        contenido = data.get('mensaje')
        mensaje.objects.create(emisor=actual, receptor=receptor, contenido=contenido)
        return JsonResponse({'status':'ok'})

def exportarChat(request, idUsuario):
    actual = request.user
    otro = User.objects.get(id=idUsuario)

    mensajes = mensaje.objects.filter(
        (Q(emisor=actual, receptor=otro))|(Q(emisor=otro, receptor=actual))
    ).order_by('fecha')
    print(mensajes)

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    width, heigh = letter

    pdf.setFont("Helvetica-Bold", 14)
    pdf.drawString(50, heigh-50, f"Chat entre {actual.username} y {otro.username}")
    pdf.setFont("Helvetica", 11)
    y = heigh - 80

    for msgInfo in mensajes:
        linea = f"[{msgInfo.fecha.strftime('%d/%m/%Y %H:%M')}] {msgInfo.emisor.username}: {msgInfo.contenido}"
        pdf.drawString(50, y, linea)
        y = y - 15
    # pdf.showPage()

    pdf.save()
    buffer.seek(0)
    nombreArchivo = f"chat_{otro.username}.pdf"
    return FileResponse(buffer, as_attachment = True, filename=nombreArchivo)

# PREGUNTA 2
# SI NO DESEA USAR EL CSRF TOKEN EN EL FRONTEND PUEDE UTILIZAR LOS DECORATORS PARA EVITAR SU USO
def publicarRespuestaComentario(request):
    # FUNCION PARA RECIBIR EL COMENTARIO DESDE EL FRONTEND
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        
        # CARGAR LOS DATOS JSON
        datos = json.loads(request.body.decode('utf-8'))


        # EXTRAER EL CONTENIDO DE LA RESPUESTA, EL ID DEL COMENTARIO PADRE Y DE LA PUBLICACION PADRE
        textoRespuesta = datos.get('respuesta')
        idComentarioPadre = datos.get('idComentario')
        idPublicacionPadre = datos.get('idPublicacion')



        # OBTENER LOS OBJETOS DE LA BASE DE DATOS
        
        objComentarioPadre = comentario.objects.get(id=idComentarioPadre)
        objPublicacion = publicacion.objects.get(id=idPublicacionPadre)


        # CREAR EL NUEVO OBJETO COMENTARIO CON EL ATRIBUTO RESPUESTA_A CONFIGURADO ADECUADAMENTE
        comentario.objects.create(
            descripcion=textoRespuesta,
            pubRel=objPublicacion,
            autoCom=request.user,
            respuesta_a=objComentarioPadre
        )





        return JsonResponse({'status': 'ok'})
    return JsonResponse({'error': 'Petición inválida'}, status=400)