from django.shortcuts import render

def inicio_view(request):
    contenido = obtener_inicio()
    return render(request, 'inicio.html', {'contenido': contenido})

def obtener_inicio():
    # Lógica para obtener los datos de la página de inicio
    return "Contenido de la página de inicio"
