from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import *
from django.http import JsonResponse
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
import random 
import datetime

def verifyToken(token):
    verifica = False
    for userTk in Token.objects.all():
        if(token==userTk.key):
            verifica = True
            
    return verifica
    
@api_view(['GET'])
def login(request):
    try: 
        correo=(request.GET['email'])
        password=(request.GET['password'])
    except:
        correo=""
        password=""
        _token="null"
    _correo=False
    if (correo==""):
        _message = "email is required"
        _status = "ERROR"
        _token = 'null'
    for user in User.objects.all():
        if (correo == user.correo):
            _correo=True
            if (check_password(password,user.password)):
                try:    
                    token = Token.objects.create(user=user)
                except: 
                    token = Token.objects.get(user=user)
                    _token = token.key
                if(status.HTTP_200_OK):
                    _status = "OK"
                    _message = "OK"
                else:
                    _status = "ERROR"
            else:
                _message = "wrong credentials"
                _status = "ERROR"
                _token = "null" 
    if(_correo==False):
         _message = "Wrong credentials"
         _status = "ERROR" 
         _token = 'null'
    
    return JsonResponse({"status":_status,"message":_message,"token":_token  })

@api_view(['GET'])
def logout(request):
    try:
        token = (request.GET['token'])
    except:
        token = "null"
    verifica = verifyToken(token)
    if (verifica):
        _status = "OK"
        _message = "Session succesfully closed."
    else:        
        _status = "ERROR"
        _message = "session_token is required"
   
    return JsonResponse({'status': _status, "message":_message})
    


def get_courses(request):
    token = (request.GET['token'])
    verifica = verifyToken(token)
    if (verifica):
        _status = "OK"
        _message = "Session succesfully closed."
        cursos = (Curso.objects.all())
        allcursos = []
        for curso in cursos:
            profesores = []
            alumnos = []
            suscripciones = Suscripcion.objects.filter(curso=curso.id)
            for sus in suscripciones:
                if (sus.tipo == 'profesor'):
                    user = User.objects.get(username=sus.user)
                    profesores.append({"first_name":user.first_name,"last_name":user.last_name})
                else:
                    user = User.objects.get(username=sus.user)
                    alumnos.append({"first_name":user.first_name,"last_name":user.last_name})

            respuesta = {
                "courseID":curso.id,
                "institutionID":curso.centro.id,
                "title":curso.nombre,
                "description":curso.descripcion,
                "subscribers":{
                    "teachers":[
                        profesores
                    ],
                    "alumns":[
                        alumnos
                    ]
                }
            }
            allcursos.append(respuesta)
            if(status.HTTP_200_OK):
                _status = "OK"
            else:
                _status = "ERROR"
    else:        
        _status = "ERROR"
        _message = "session_token is required"
        allcursos = 'null'

    
    return JsonResponse({"status":_status,"message":_message,"course_list":allcursos}, safe=False,status=status.HTTP_200_OK)

@api_view(['GET'])
def get_course_details(request):
    try:
        token = (request.GET['token'])
        
    except:
        token = "null"
    verifica = verifyToken(token)
    if (verifica):
        cursos = (Curso.objects.all())
        _curso = request.GET['courseID']
        _recursos = []
        uploads = []
        resp = False
        for curso in cursos:
            if (_curso == str(curso.id)):
                resp = True
                recursos = Recurso.objects.filter(curso=curso.id)
                for recurso in recursos:
                    _recursos.append(recurso.titulo)
                _entrega = {}
                tascas = []
                for _tarea in Tarea.objects.filter(curso = curso.id):
                    uploads = []
                    for entrega in Entrega.objects.filter(tarea=_tarea.id):
                        pathfile = str(entrega.archivo)
                        calificacion = Calificacion.objects.filter(tarea=_tarea.id).first()
                        _entrega = {
                            "studentID":entrega.user.id,
                            "text":_tarea.nombre,
                            "file":pathfile,
                            "grade":calificacion.nota,
                            "feedback":calificacion.comentario_profesor
                        }
                        uploads.append(_entrega)
                    tasca = {
                        "ID":_tarea.nombre,
                        "type":"file",
                        "descripcion":_tarea.nombre,
                        "uploads":uploads
                    }
                    tascas.append(tasca)
                _vrtasks = []
                for _vrtarea in VRTarea.objects.filter(curso= curso.id):
                                        
                    completions= []
                    
                    for entrega in Entrega.objects.filter(id = _vrtarea.id):
                        print(Calificacion.objects.filter(vrtarea= _vrtarea.id))
                        calificacion = Calificacion.objects.filter(vrtarea = entrega.id).first()
                        _entrega = {
                            "studentID":entrega.user.id,
                            "position_data":_vrtarea.performance_data,
                            "autograde":_vrtarea.autograde,
                            "grade": calificacion.nota,
                            "feedback": calificacion.comentario_profesor
                        }
                        completions.append(_entrega)
                    vrtasca = {
                        "ID":_vrtarea.id,
                        "title":_vrtarea.exercise.nombre,
                        "descripcion":_vrtarea.exercise.descripcion,
                        "VRexId":"_vrtarea.exercise.id",
                        "versionID":_vrtarea.version,
                        "completions": completions
                    }
                    _vrtasks.append(vrtasca)

                _course = {
                    "title": curso.nombre,
                    "description":curso.descripcion,
                    "courseID": curso.id,
                    "institutionID": curso.centro.id,
                    "elements": _recursos,
                    "tasks": tascas, 
                    "vrtasks":_vrtasks  
                }
        if(status.HTTP_200_OK):
            _status = "OK"
            _message = "OK"
        else:
            _status = "ERROR"
            _message = "failed request"
        if (resp == False):
            _message = "course no found"
            _course = "null"  
    else :
        _status = "ERROR"
        _message = "token required"
        _course = 'null'
          
    return JsonResponse({"status":_status,"message":_message,"course":_course}, safe=False,status=status.HTTP_200_OK)
 
@api_view(['GET'])
def pin_request(request):
    token = (request.GET['token'])
    task = (request.GET['task'])
    verifica = verifyToken(token)
    pinexiste = True
    if (verifica):
        for entrega in Entrega.objects.all():
            if (task == str(entrega.id)):
                if (entrega.pin==None):
                    while (pinexiste==True):
                        pinexiste = False
                        newpin = random.randint(0,9999)
                        for entr in Entrega.objects.all():
                            if(newpin == entr.pin):
                                pinexiste = True
                        if (pinexiste == False):
                            break
                    pin = newpin
                    entrega.pin = newpin
                    entrega.save()
                else:
                    pin = entrega.pin
        entrega = Entrega.objects.filter(id=task).first()
        _status = "OK"
        _message = "token va bien"
    else:
        _status = "ERRROR" 
        _message = "invalid token"   

    return JsonResponse({"status":_status,"message":_message,"PIN":entrega.pin})

@api_view(['GET'])
def start_vr_exercise(request):
    pin = (request.GET['pin'])
    exer = False
    for entrega in Entrega.objects.all():
        if (pin==str(entrega.pin)):
            exer = True
            _username = (entrega.user.username)
            _VRexerciseID = (entrega.vrtarea.exercise.id)
            _minExerciseVersion = (entrega.vrtarea.minversion)
            if(status.HTTP_200_OK):
                _status = "OK"
                _message = "OK"
            else:
                exer = False
                _status = "ERROR"
                _message = "failed request"
    if exer ==   False:
        _status="OK"
        _message = "invalid PIN"  
        _username = "null"
        _VRexerciseID = "null"
        _minExerciseVersion = "null"
    return JsonResponse({"status":_status,
                        "message":_message,
                        "username":_username,
                        "VRexerciseID":_VRexerciseID,
                        "minExerciseVersion":_minExerciseVersion})

#Send values as request HEADER
@api_view(['POST'])
def finish_vr_exercise(request):
    _status="ERROR"
    try :
            pin = (request.headers['pin'])
    except: 
            pin = "null"
    try:             
        autograde = (request.headers['autograde'])
    except:
        autograde = "null"
    try: 
        vrexerciseid = (request.headers['exerciseID'])
    except:
        vrexerciseid = "null"
    try:
        exerciseversion = (request.headers['version'])
    except:
        exerciseversion = "null"
    try:
        performancedata = (request.headers['performance'])
    except: 
        performancedata = "null"
    if(pin=="null"):
        _message = "Missing pin"
    elif(autograde == "null"):
        _message = "Missing autograde"
    elif(vrexerciseid == "null"):
        _message = "Missing vrexerciseid"
    elif(exerciseversion == "null"):
        _message = "Missing exerciseversion"
    elif(performancedata == "null"):
        _message = "Missing performancedata"
    else:
        lastvr =  VRTarea.objects.all().order_by('-id')[0]
        newid = lastvr.id+1
        entrega =  Entrega.objects.filter(pin=pin)
        _ejercicio = Ejercicio.objects.filter(id = vrexerciseid)[0]
        newvrtarea = VRTarea.objects.get_or_create(id=newid, nombre = pin, autograde = autograde, performance_data = performancedata, version = exerciseversion, exercise = _ejercicio, curso=_ejercicio.curso )
        
        _status = "OK"
        _message = "Exercise data succesfully stored"

    if not (status.HTTP_200_OK):
        _status = "ERROR"
        _message = "failed request"
    
    return JsonResponse({"status": _status, "message":_message})

            
