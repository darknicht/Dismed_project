from django.shortcuts import render
from django.db import connection

def buscador_view(request):
    if request.method == 'POST':
        # Obtener los datos del formulario de búsqueda y realizar la búsqueda
        query = request.POST.get('query')
        resultados = buscar(query)
        return render(request, 'buscador.html', {'resultados': resultados})
    else:
        return render(request, 'buscador.html')
def buscar(query):
    # Lógica para realizar la búsqueda en la base de datos
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM unidadesmd WHERE nombre_unidad LIKE %s", [f'%{query}%'])
        resultados = cursor.fetchall()
    return resultados


