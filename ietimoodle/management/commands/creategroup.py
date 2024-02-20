import logging
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from ietimoodle.models import User

GROUPS = ['AdministradorDeCentros','Profesor']
MODELS = ['user','curso','entrega','ejercicio']
PERMISSIONS = ['view', 'add','delete','change' ]  # For now only view permission by default for all, others include add, delete, change

class Command(BaseCommand):
    help = 'Crea el grupo AdministradorDeCentros con todos los permisos sobre los modelos Usuarios y Cursos'

    def handle(self, *args,**options):
        for group in GROUPS:
            new_group, created = Group.objects.get_or_create(name=group)
            for model in MODELS:
                for permission in PERMISSIONS:
                    name = 'Can {} {}'.format(permission, model)
                    print("Creating {}".format(name))

                    try:
                        model_add_perm = Permission.objects.get(name=name)
                    except Permission.DoesNotExist:
                        logging.warning("Permission not found with name '{}'.".format(name))
                        continue
                    new_group.permissions.add(model_add_perm)
        print("Created default group and permissions.")
            

    