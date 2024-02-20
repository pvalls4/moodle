import re
from django.shortcuts import render,  get_object_or_404, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
from django.http import HttpResponse, HttpResponseNotFound
from .forms import LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse

from .models import *
from .serializers import * 
from rest_framework import viewsets
from django.contrib.auth.models import Permission
from rest_framework import permissions
import os, mimetypes


class MyAuthForm(AuthenticationForm):
	error_messages = {
		'invalid_login': _(
			"Asegurate de introducir el correo y la contraseña correctamente."
			" Ten en cuenta las máyusculas."
		),
		'inactive': _("El ususario no esta activo"),
	}


class LoginView(auth_views.LoginView):
	form_class = LoginForm
	authentication_form = MyAuthForm
	template_name = 'registration/login.html'

def home(request):
	return render(request, 'home.html')

def logout_view(request):
	logout(request)
	return render(request, "logout.html")

@login_required
def download(request, element, filename=''):
	if filename != '':
		try:
			BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
			filepath = BASE_DIR + '/archivos/' + element + '/' + filename
			path = open(filepath, 'rb')
			mime_type, _ = mimetypes.guess_type(filepath)
			response = HttpResponse(path, content_type=mime_type)
			response['Content-Disposition'] = "attachment; filename=%s" % filename
			return response
		except FileNotFoundError:
			return HttpResponseNotFound('Error 404 File not found')
	else:
		return render(request, 'file.html')

@login_required
def dashboard(request):
	suscripciones=Suscripcion.objects.filter(user=request.user.pk)
	cursos=Curso.objects.all
	content={
		'suscripciones': suscripciones,
		'cursos':cursos,
	}
	return render(request, 'dashboard.html', content)

@login_required
def grade(request, cursoid):
	recursos = Recurso.objects.filter(curso=cursoid)
	tareas = Tarea.objects.filter(curso=cursoid)
	vrtareas = VRTarea.objects.filter(curso=cursoid)
	role= Suscripcion.objects.filter(curso=cursoid, user=request.user.pk)[0]
	alumnos= Suscripcion.objects.filter(curso=cursoid,tipo='alumno')[0]
	firstAlId=get_object_or_404(User, pk=alumnos.user.pk)
	content= {
		'resources': recursos,
		'tasks': tareas,
		'vrtasks': vrtareas,
		'role': role,
		'grade': get_object_or_404(Curso, pk=cursoid),
		'firstal': firstAlId
	}
	return render(request, 'grade.html', content)

@login_required
def qualifications(request, cursoid):
	alumn=get_object_or_404(User, pk=request.user.pk)
	tasks = Tarea.objects.filter(curso=cursoid)
	vrtasks = VRTarea.objects.filter(curso=cursoid)
	deliveries=Entrega.objects.filter(user=alumn.pk, curso=cursoid)
	qualifications=[]
	for t in tasks:
		try:
			qualifications.append(Calificacion.objects.filter(user=alumn.pk, tarea=t.pk))
		except:
			continue
	vrqualifications=[]
	for vrt in vrtasks:
		try:
			vrqualifications.append(VRCalificacion.objects.filter(user=alumn.pk, vrtarea=vrt.pk))
		except:
			continue
	deliveriesRealizadas=[]
	deliveriesVRRealizadas=[]
	for d in deliveries:
		try:
			deliveriesRealizadas.append(d.tarea.pk)
		except:
			continue
	for d in deliveries:
		try:
			deliveriesVRRealizadas.append(d.vrtarea.pk)
		except:
			continue
	content= {
		'grade': get_object_or_404(Curso, pk=cursoid),
		'alumn': alumn,
		'tasks': tasks,
		'vrtasks': vrtasks,
		'deliveries': deliveries,
		'qualifications': qualifications,
		'vrqualifications': vrqualifications,
		'deliveriesRealizadas': deliveriesRealizadas,
		'deliveriesVRRealizadas': deliveriesVRRealizadas,
	}
	return render(request, 'qualifications.html', content)

@login_required
def resource(request, resourceid):
	resource=get_object_or_404(Recurso, pk=resourceid)
	curso=get_object_or_404(Curso, pk=resource.curso.pk)
	content= {
		'resource': resource,
		'curso': curso
	}
	return render(request, 'resource.html', content)

@login_required
def task(request, taskid):
	task=get_object_or_404(Tarea, pk=taskid)
	curso=get_object_or_404(Curso, pk=task.curso.pk)
	alumn=get_object_or_404(User, pk=request.user.pk)
	qualification=Calificacion.objects.filter(user=alumn.pk, tarea=task.pk)
	tasks=Tarea.objects.filter(curso=curso.pk)
	vrtasks=VRTarea.objects.filter(curso=curso.pk)
	entrega=Entrega.objects.filter(tarea=taskid, user=alumn.pk)
	content= {
		'task': task,
		'curso': curso,
		'entrega': entrega,
		'qualification': qualification,
		'tasks': tasks,
		'vrtasks': vrtasks
	}
	return render(request, 'task.html', content)

@login_required
def vrtask(request, taskid):
	task=get_object_or_404(VRTarea, pk=taskid)
	curso=get_object_or_404(Curso, pk=task.curso.pk)
	alumn=get_object_or_404(User, pk=request.user.pk)
	qualification=VRCalificacion.objects.filter(user=alumn.pk, vrtarea=task.pk)
	tasks=Tarea.objects.filter(curso=curso.pk)
	vrtasks=VRTarea.objects.filter(curso=curso.pk)
	entrega=Entrega.objects.filter(vrtarea=taskid, user=alumn.pk)
	content= {
		'task': task,
		'curso': curso,
		'entrega': entrega,
		'qualification': qualification,
		'tasks': tasks,
		'vrtasks': vrtasks,
	}
	return render(request, 'vrtask.html', content)

@login_required
def addDelivery(request, taskid):
	task=get_object_or_404(Tarea, pk=taskid)
	grade=get_object_or_404(Curso, pk=task.curso.pk)
	user=get_object_or_404(User, pk=request.user.pk)
	tasks=Tarea.objects.filter(curso=grade.pk)
	curso=get_object_or_404(Curso, pk=task.curso.pk)
	vrtasks=VRTarea.objects.filter(curso=curso.pk)
	delivery=Entrega.objects.filter(tarea=taskid, user=user.pk)
	content= {
		'task': task,
		'grade': grade,
		'delivery': delivery,
		'tasks': tasks,
		'vrtasks': vrtasks,
		'vr': False
	}
	return render(request, 'addDelivery.html', content)

@login_required
def addDeliveryVr(request, taskid):
	task=get_object_or_404(VRTarea, pk=taskid)
	grade=get_object_or_404(Curso, pk=task.curso.pk)
	user=get_object_or_404(User, pk=request.user.pk)
	tasks=Tarea.objects.filter(curso=grade.pk)
	curso=get_object_or_404(Curso, pk=task.curso.pk)
	vrtasks=VRTarea.objects.filter(curso=curso.pk)
	delivery=Entrega.objects.filter(vrtarea=taskid, user=user.pk)
	content= {
		'task': task,
		'grade': grade,
		'delivery': delivery,
		'tasks': tasks,
		'vrtasks': vrtasks,
		'vr': True
	}
	return render(request, 'addDelivery.html', content)

@login_required
def delivery(request, taskid, alumnid):
	alumn= get_object_or_404(User, pk=alumnid)
	task=get_object_or_404(Tarea, pk=taskid)
	curso=get_object_or_404(Curso, nombre=task.curso)
	vr = False

	try:
		deliveries=Entrega.objects.filter(tarea=taskid, user=alumnid)
		alumnos= Suscripcion.objects.filter(curso=curso.pk, tipo="alumno")
		qualification=Calificacion.objects.filter(tarea=taskid, user=alumnid)
		alumnosCurso = []
		for a in alumnos:
			alumnosCurso.append(a.user.pk)
		if alumnosCurso.index(alumnid) == len(alumnosCurso)-1:
			nextAlumn=alumnosCurso[0]
		else:
			nextAlumn=alumnosCurso[alumnosCurso.index(alumnid)+1]
		
		if alumnosCurso.index(alumnid) == 0:
			prevAlumn=alumnosCurso[-1]
		else:
			prevAlumn=alumnosCurso[alumnosCurso.index(alumnid)-1]
	except:
		deliveries=""
		prevAlumn=""
		nextAlumn=""
	
	
	content = {
		'alumn': alumn,
		'task': task,
		'deliveries': deliveries,
		'nextAlumn': nextAlumn,
		'prevAlumn': prevAlumn,
		'qualification': qualification,
		'curso': curso,
		'vr': vr,
	}
	return render(request, 'delivery.html', content)

@login_required
def vrdelivery(request, taskid, alumnid):
	alumn= get_object_or_404(User, pk=alumnid)
	task=get_object_or_404(VRTarea, pk=taskid)
	curso=get_object_or_404(Curso, nombre=task.curso)
	try:
		deliveries=Entrega.objects.filter(vrtarea=taskid, user=alumnid)
		alumnos= Suscripcion.objects.filter(curso=curso.pk, tipo="alumno")
		qualification=VRCalificacion.objects.filter(vrtarea=taskid, user=alumnid)
		alumnosCurso = []
		for a in alumnos:
			alumnosCurso.append(a.user.pk)
		if alumnosCurso.index(alumnid) == len(alumnosCurso)-1:
			nextAlumn=alumnosCurso[0]
		else:
			nextAlumn=alumnosCurso[alumnosCurso.index(alumnid)+1]
		
		if alumnosCurso.index(alumnid) == 0:
			prevAlumn=alumnosCurso[-1]
		else:
			prevAlumn=alumnosCurso[alumnosCurso.index(alumnid)-1]
	except:
		deliveries=""
		prevAlumn=""
		nextAlumn=""
	
	
	content = {
		'alumn': alumn,
		'task': task,
		'deliveries': deliveries,
		'nextAlumn': nextAlumn,
		'prevAlumn': prevAlumn,
		'qualification': qualification,
		'curso': curso,
	}
	return render(request, 'delivery.html', content)

@login_required
def fastCorrection(request, taskid):
	task=get_object_or_404(Tarea, pk=taskid)
	curso=get_object_or_404(Curso, nombre=task.curso)
	deliveries=Entrega.objects.filter(tarea=task.pk)
	alumnos= Suscripcion.objects.filter(curso=curso.pk, tipo="alumno")
	qualifications=Calificacion.objects.filter(tarea=task.pk)
	alumnosEntregado=[]
	vr=False
	for d in deliveries:
		alumnosEntregado.append(d.user.pk)
	
	content = {
		'alumnos': alumnos,
		'task': task,
		'deliveries': deliveries,
		'alumnosEntregado': alumnosEntregado,
		'qualifications': qualifications,
		'curso': curso,
		'vr':vr,
	}
	return render(request, 'fastCorrection.html', content)

@login_required
def fastCorrectionVr(request, taskid):
	task=get_object_or_404(VRTarea, pk=taskid)
	curso=get_object_or_404(Curso, nombre=task.curso)
	deliveries=Entrega.objects.filter(vrtarea=task.pk)
	alumnos= Suscripcion.objects.filter(curso=curso.pk, tipo="alumno")
	curso=get_object_or_404(Curso, pk=task.curso.pk)
	qualifications=VRCalificacion.objects.filter(vrtarea=taskid)
	alumnosEntregado=[]
	vr=True
	for d in deliveries:
		alumnosEntregado.append(d.user.pk)
	
	content = {
		'alumnos': alumnos,
		'task': task,
		'deliveries': deliveries,
		'alumnosEntregado': alumnosEntregado,
		'qualifications': qualifications,
		'curso': curso,
		'vr':vr,
	}
	return render(request, 'fastCorrection.html', content)

@csrf_exempt
def actualizarEjercicioIndiviual(request, qualificationID, nota, comentarioProfesor):
	qualification = get_object_or_404(Calificacion, pk=qualificationID)
	qualification.nota = nota
	qualification.comentario_profesor = comentarioProfesor
	qualification.save()
@csrf_exempt
def actualizarEjercicioIndiviualVR(request, qualificationID, nota, comentarioProfesor):
	qualification = get_object_or_404(VRCalificacion, pk=qualificationID)
	qualification.nota = nota
	qualification.comentario_profesor = comentarioProfesor
	qualification.save()

@csrf_exempt
def actualizar(request, entrega, nota, comentarioProfesor):
	delivery = get_object_or_404(Calificacion, pk=entrega)
	delivery.nota = nota
	delivery.comentario_profesor = comentarioProfesor
	delivery.save()
