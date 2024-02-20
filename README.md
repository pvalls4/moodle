# classVRroom
# Nosotros

Componentes del grupo:

    - Guillem Albo Pintor
        albopintor@gmail.com

    - Pau Valls Vilalta
        pvallsvilalta@gmail.com

    - Sergio de la Torre Rins
        sergiorins@gmail.com

## Descripcion

L'IES Esteve Terradas i Illa (IETI) participa a un projecte del Ministerio de Educación y FP anomenat VR Salud. En aquest es desenvoluparà una aplicació immersiva de Realitat Virtual (RV) per a estudiants d'auxiliar d'infermeria. En aquesta App VR es realitzaran exercicis de mobilització de pacients i un vestit de MoCap (Motion Capture) ens permetrà conèixer amb precisió la posició de l'usuari. D'aquesta manera es podrà determinar la idoneitat de la postura adoptada (higiene postural) i es podrà donar una resposta immediata a l'usuari sobre possibles riscos de lesió.

El IETI contribuirà amb el software classVRroom, de tipus LMS (Learning Management System, el més conegut del qual és el Moodle) per a fer seguiment i qualificació dels exercicis completats per l'alumnat.

## Instalación

Crea un entorno virtual para python 3

    https://conpilar.es/como-crear-un-entorno-virtual-python-3-en-ubuntu-20-04/

Descargar repositorio github:


Entrar en el entorno virtual de Python:
    - source /env/bin/activate
    
Instalamos las dependencias:
    - pip install -r requirements.txt

Poblar la base de datos:

    python3 manage.py createsuperuser
    
    -- definir las credenciales del superusuario "Username" y "Password"

    python3 manage.py creategroup

Y aplicar los cambios:

    python3 manage.py makemigrations

    python3 manage.py migrate     

