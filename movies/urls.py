from django.urls import path
from . import views

urlpatterns=[
    path('',views.home_page,name='home_page'),  # cuando alguien ingresa al link de la app, sin ningun tipo de / o comando
    # django corre este codigo, y dice el path('') , es decir, vacio , coincide , entonces corre views.home_page
    path('create/' , views.create, name='create'),
    path('edit/<str:movie_id>', views.edit, name='edit'), # yourapp.com/edit/rec57690i8t5 , este id se obtiene del {% url ..} del edit modal.html
    path('delete/<str:movie_id>', views.delete, name='delete')
]
