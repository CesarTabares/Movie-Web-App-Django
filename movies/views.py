from django.shortcuts import render, redirect
from django.contrib import messages # importante para notificaciones
from airtable import Airtable
import os

#debemos hablar a la API de Air Table y conectarnos

AIRTABLE_API_KEY='keyeTFWCn9H7zwNRG'  #esto se pego en esta parte pq corriendo la app de manera local generaba un error, esto implico
# en las lineas de abajo de AT=.... luego del get, complementar con estas variables.
AIRTABLE_MOVIESTABLE_BASE_ID='appe0PgrgJID0IYe2'

AT = Airtable(os.environ.get('AIRTABLE_MOVIESTABLE_BASE_ID', AIRTABLE_MOVIESTABLE_BASE_ID),'Movies',
             api_key=os.environ.get('AIRTABLE_API_KEY ',AIRTABLE_API_KEY))

# Create your views here.
def home_page(request):
    user_query= str(request.GET.get('query','')) # queremos capturar la query para luego buscarla
    #en la base de datos
    search_result= AT.get_all(formula="FIND('" + user_query.lower() +"',LOWER({Name}))")
    stuff_for_frontend={'search_result': search_result} #generalmente llamado context dictionary en django,
    return render(request,'movies/movies_stuff.html', stuff_for_frontend)


def create(request):
    if request.method=='POST':
        data={
            'Name': request.POST.get('name'),
            'Pictures':[{'url': request.POST.get('url')or 'https://images-na.ssl-images-amazon.com/images/I/31qWM5qyeDL._SX258_BO1,204,203,200_.jpg'}] , # truco de python con or, siempre escoge el primero a no ser que el primero sea 0 o vacio y ahi pasa al segundo
            'Rating': int(request.POST.get('rating')),
            'Notes': request.POST.get('notest')
        }
        try:
            response = AT.insert(data)
        #notify on create
            messages.success(request,'New Movie Added: {}'.format(response['fields'].get('Name'))) #el get es utilizado como otra forma de indexar un diccionario, es decir aca hubiera sido lo mismo decir response['fields']['Name'] , la ventaja del get es que si buscamos una llave que no existe, el programa no genera un error fatal para el programa, de la otra forma si, si no existe la llave buscada, ignora el codigo y ya.
        except Exception as e:
                messages.warning(request,'Got an error when trying to create a new movie: {}'.format(e))

    return redirect('/')

def edit(request,movie_id):
    print('edit function')

    if request.method == 'POST':
        data={
            'Name':request.POST.get('name'), # name obtenido de edit-model campo name
            'Pictures': [{'url':request.POST.get('url')}],
            'Rating':int(request.POST.get('rating')),
            'Notes': request.POST.get('notes'),
        }

        try:
            response= AT.update(movie_id,data)
            #notify on update
            messages.success(request,'Edited Movie: {}'.format(response['fields'].get('Name')))
        except Exception as e:
                messages.warning(request, 'Got an error when trying to uptdate a movie: {}'.format(e))
    return redirect('/')

def delete(request,movie_id):
    print('delete function')

    try:
        movie_name= AT.get(movie_id)['fields'].get('Name')
        response= AT.delete(movie_id)
        #notify on delete
        messages.warning(request,'Deleted Movie: {}'.format(movie_name))
    except Exception as e:
        messages.warning(request,'Got an error when trying to delete a movie: {}'.format(e))
    return redirect('/')
