from django.urls import path
from .views import register, login_view, logout_view

from . import views  # Asegúrate de importar las vistas desde tu aplicación


from .views import (
    IndexView,
    AdminView,
    AboutView,
    ComentarioView,
    ObtenerAutoresView,
    ObtenerLibrosView,
    AgregarAutorView,
    AgregarLibroView,
    EliminarAutorView,
    EliminarLibroView,
    EditarAutorView,
    EditarLibroView,
    AgregarComentarioView,
    ObtenerComentariosView,
    ObtenerMisComentariosView,
    EliminarComentarioView,
    ModificarComentarioView
)

urlpatterns = [
    path('', views.login_view, name='login'),  # Ruta para la vista principal
    
    path('obtener-autores/', ObtenerAutoresView.as_view(), name='obtener_autores'),  # Obtener lista de autores
    path('obtener-libros/', ObtenerLibrosView.as_view(), name='obtener_libros'),  # Obtener lista de libros
    path('agregar-autor/', AgregarAutorView.as_view(), name='agregar_autor'),  # Agregar un nuevo autor
    path('agregar-libro/', AgregarLibroView.as_view(), name='agregar_libro'),  # Agregar un nuevo libro
    path('eliminar-autor/<int:pk>/', EliminarAutorView.as_view(), name='eliminar_autor'),  # Eliminar un autor
    path('eliminar-libro/<int:pk>/', EliminarLibroView.as_view(), name='eliminar_libro'),  # Eliminar un libro
    path('obtener-autor/<int:pk>/', EditarAutorView.as_view(), name='obtener_autor'), #Obtener un autor
    path('editar-autor/<int:pk>/', EditarAutorView.as_view(), name='editar_autor'), #Editar autor
    path('obtener-libro/<int:pk>/', EditarLibroView.as_view(), name='obtener_libro'), #Obtener un libro
    path('editar-libro/<int:pk>/', EditarLibroView.as_view(), name='editar_libro'), #Editar libro
    
    #Para llevar a diferentes páginas
    path("index/", IndexView.as_view(), name='index'),
    path("administrador/", AdminView.as_view(), name='administador'),
    path("registro/", register, name="registro"),
    path("login/", login_view, name="login"),
    path('logout/', logout_view, name='logout'),
    path('about/', AboutView.as_view(), name='about'),
    path('comentario/', ComentarioView.as_view(), name='comentario'),
    
    path('obtener-comentarios/<str:libro_isbn>/', ObtenerComentariosView.as_view(), name='obtener_comentarios'),
    path('agregar-comentario/<str:libro_isbn>/', AgregarComentarioView.as_view(), name='agregar_comentario'),
    path('obtener-mis-comentarios/', ObtenerMisComentariosView.as_view(), name='obtener_mis_comentarios'),
    path('modificar-comentario/<int:comentario_id>/', ModificarComentarioView.as_view(), name='modificar_comentario'),
    path('eliminar-comentario/<int:comentario_id>/', EliminarComentarioView.as_view(), name='eliminar_comentario'),
    
]