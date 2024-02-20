from django.urls import path,include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework.authtoken import views as apiviews
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import routers
from rest_framework import routers, serializers, viewsets
from .models import *
from .serializers import *
from django.core import serializers
import json 
from . import api

app_name='moodle'   

urlpatterns = [
    path('', views.home, name='home'),
    path('logout', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('archivos/<str:element>/<str:filename>', views.download, name='download'),
    path('grade/<int:cursoid>', views.grade, name='grade'),
    path('qualifications/<int:cursoid>', views.qualifications, name='qualifications'),
    path('resource/<int:resourceid>', views.resource, name='resource'),
    path('task/<int:taskid>', views.task, name='task'),
    path('vrtask/<int:taskid>', views.vrtask, name='vrtask'),
    path('ad/<int:taskid>', views.addDelivery, name='addDelivery'),
    path('advr/<int:taskid>', views.addDeliveryVr, name='addDeliveryVr'),
    path('fc/<int:taskid>', views.fastCorrection, name='fastCorrection'),
    path('vr/fc/<int:taskid>', views.fastCorrectionVr, name='fastCorrectionVr'),
    path('<int:taskid>/<int:alumnid>', views.delivery, name='delivery'),
    path('vr/<int:taskid>/<int:alumnid>', views.vrdelivery, name='vrdelivery'),
    path('api/login',api.login),
    path('api/logout',api.logout),
    path('api/get_courses',api.get_courses),
    path('api/get_course_details',api.get_course_details),
    path('api/pin_request',api.pin_request),
    path('api/start_vr_exercise',api.start_vr_exercise), 
    path('api/finish_vr_exercise',api.finish_vr_exercise),
    path('actualizar/<int:qualificationID>/<int:nota>/<str:comentarioProfesor>',views.actualizarEjercicioIndiviual, name="actualizarEjercicio"),
    path('actualizar/vr/<int:qualificationID>/<int:nota>/<str:comentarioProfesor>',views.actualizarEjercicioIndiviualVR, name="actualizarEjercicioVR"),
    path('actualizar/<int:entrega>/<int:nota>/<str:comentarioProfesor>',views.actualizar, name="actualizar"),

]

urlpatterns += staticfiles_urlpatterns()
