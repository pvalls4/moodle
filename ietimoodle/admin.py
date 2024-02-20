from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin 
from django.conf import settings
from django.contrib.auth.forms import UserChangeForm
from django.utils.translation import gettext_lazy as _

class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	fieldsets = (
		(None, {'fields': ('username','correo', 'password', )}),
		(_('Información Personal'), {'fields': ('first_name', 'last_name')}),
		(_('Permisos'), {'fields': ('is_active', 'is_staff', 'is_superuser',
										'groups', 'user_permissions')}),
		(_('Datos Relevantes'), {'fields': ('last_login', 'date_joined')}),
		(_('Información Usuario'), {'fields': ('centro', 'privacidad')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide', ),
			'fields': ('username','correo', 'password1', 'password2'),
		}),
	)
	list_display = ['username','correo', 'first_name', 'last_name', 'is_staff']
	search_fields = ('username','correo', 'first_name', 'last_name')
	ordering = ('correo', )


class SuscripiconesInLine(admin.TabularInline):
	model = Suscripcion
	extra = 1
	
class EntrgaInLine(admin.TabularInline):
	model = Entrega
	extra = 1
class RecursoInLine(admin.TabularInline):
	model = Recurso
	extra = 1
class TareaInLine(admin.TabularInline):
	model = Tarea
	extra = 1
class TareaVrInLine(admin.TabularInline):
	model = VRTarea
	extra = 1


class CursoAdmin(admin.ModelAdmin):
	list_display = ('nombre','descripcion','centro')
	inlines =[
		SuscripiconesInLine,
		TareaInLine,
		EntrgaInLine,
		RecursoInLine,
		TareaVrInLine,
	]

class CalifcationsInLine(admin.TabularInline):
    model = Calificacion
    extra = 1

class TareaAdmin(admin.ModelAdmin):
    list_display = ('nombre','ponderacion','visibilidad')
    inlines = [
		CalifcationsInLine,
	]
    
class VRCalifcationsInLine(admin.TabularInline):
    model = VRCalificacion
    extra = 1

class VRTareaAdmin(admin.ModelAdmin):
    list_display = ('nombre','ponderacion','visibilidad')
    inlines = [
		VRCalifcationsInLine,
	]

admin.site.register(Centro) 
admin.site.register(Curso,CursoAdmin)
admin.site.register(Ejercicio)
admin.site.register(Tarea,TareaAdmin)
admin.site.register(NivelPrivacidad) 
admin.site.register(User, UserAdmin)
admin.site.register(Entrega) 
admin.site.register(Suscripcion)
admin.site.register(Recurso)
admin.site.register(Calificacion)
admin.site.register(VRCalificacion)
admin.site.register(VRTarea)

