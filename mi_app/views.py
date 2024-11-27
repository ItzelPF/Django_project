from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.generic import View, ListView, CreateView, DeleteView
from django.contrib.auth import logout

#Para registrar y logins
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, AuthenticationForm

#Importar modelos
from django.core import serializers
from .models import Autor, Libro, Comentario
from mi_app.forms import AutorForm, LibroForm

class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')

class AdminView(View):
    def get(self, request):
        return render(request, 'admin.html')
    
class AboutView(View):
    def get(self, request):
        return render(request, 'about.html')

class ComentarioView(View):
    def get(self, request):
        return render(request, 'comentario.html')

class ObtenerAutoresView(ListView):
    model = Autor

    def get(self, request, *args, **kwargs):
        autores = self.get_queryset()
        data = [{'id': autor.id, 'nombre': autor.nombre} for autor in autores]
        return JsonResponse({'data': data})
    

class ObtenerLibrosView(ListView):
    model = Libro
    def get(self, request, *args, **kwargs):
        libros = self.get_queryset()
        data = [{'id': libro.id, 'titulo': libro.titulo, 'autor': libro.autor.nombre,
                 'editorial': libro.editorial, 'anio': libro.anio, 'isbn':libro.isbn} for libro in libros]
        return JsonResponse({'data': data})

class AgregarAutorView(CreateView):
    model = Autor
    form_class = AutorForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({'status': 'ok'})

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors})

class AgregarLibroView(CreateView):
    model = Libro
    form_class = LibroForm

    def form_valid(self, form):
        form.save()
        return JsonResponse({'status': 'ok'})

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors})

class EliminarAutorView(DeleteView):
    model = Autor

    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            return JsonResponse({'status': 'ok'})
        except self.model.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Autor no encontrado'})

class EliminarLibroView(DeleteView):
    model = Libro
    def delete(self, request, *args, **kwargs):
        try:
            self.get_object().delete()
            return JsonResponse({'status': 'ok'})
        except self.model.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Libro no encontrado'})
 
class EditarAutorView(View):
    def get(self, request, pk):
        autor = get_object_or_404(Autor, pk=pk)
        return JsonResponse({'id': autor.id, 'nombre': autor.nombre})

    def post(self, request, pk):
        autor = get_object_or_404(Autor, pk=pk)
        nuevo_nombre = request.POST.get('nombre')
        autor.nombre = nuevo_nombre
        autor.save()
        return JsonResponse({'status': 'ok'})

class EditarLibroView(View):
    def get(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        return JsonResponse({
            'id': libro.id,
            'titulo': libro.titulo,
            'editorial': libro.editorial,
            'anio': libro.anio,
            'isbn': libro.isbn,
            'autor': {'id': libro.autor.id, 'nombre': libro.autor.nombre}
        })

    def post(self, request, pk):
        libro = get_object_or_404(Libro, pk=pk)
        titulo = request.POST.get('titulo')
        autor_id = request.POST.get('autor')
        autor = get_object_or_404(Autor, pk=autor_id)
        editorial = request.POST.get('editorial')
        anio = request.POST.get('anio')
        isbn = request.POST.get('isbn')
        
        libro.titulo = titulo
        libro.autor = autor
        libro.editorial = editorial
        libro.anio = anio
        libro.isbn = isbn
        libro.save()

        return JsonResponse({'status': 'ok'})

        
#vista registro
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Por favor corrige los errores a continuación.")
    else:
        form = CustomUserCreationForm()
    return render(request, "registro.html", {"form": form})

#vista login
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)  # Cierra la sesión del usuario
    return redirect('login')

class AgregarComentarioView(View):
    def post(self, request, libro_isbn):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'mensaje': 'Usuario no autenticado.'}, status=403)
        
        libro = get_object_or_404(Libro, isbn=libro_isbn)
        usuario = request.user

        # Evita duplicados
        if Comentario.objects.filter(libro=libro, usuario=usuario).exists():
            return JsonResponse({'status': 'error', 'mensaje': 'Ya has comentado este libro.'})

        comentario_texto = request.POST.get('comentario')
        if comentario_texto:
            comentario = Comentario.objects.create(libro=libro, usuario=usuario, comentario=comentario_texto)
            return JsonResponse({'status': 'success', 'comentario': comentario.comentario, 'usuario': usuario.username})
        
        return JsonResponse({'status': 'error', 'mensaje': 'El comentario no puede estar vacío.'})
    
class ObtenerComentariosView(View):
    def get(self, request, libro_isbn):
        libro = get_object_or_404(Libro, isbn=libro_isbn)

        # Obtener solo los comentarios del usuario logueado
        comentarios = Comentario.objects.filter(libro=libro, usuario=request.user)

        comentarios_data = [{
            'usuario': comentario.usuario.username,
            'comentario': comentario.comentario,
        } for comentario in comentarios]

        return JsonResponse({'data': comentarios_data})
    
class ObtenerMisComentariosView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'error', 'mensaje': 'Usuario no autenticado.'}, status=403)
        
        usuario = request.user
        comentarios = Comentario.objects.filter(usuario=usuario).select_related('libro')

        comentarios_data = [
            {
                'id': comentario.id,
                'libro': {
                    'titulo': comentario.libro.titulo,
                    'autor': comentario.libro.autor.nombre,  # Ajusta el acceso a la relación
                    'editorial': comentario.libro.editorial,
                    'anio': comentario.libro.anio,
                    'isbn': comentario.libro.isbn,
                },
                'comentario': comentario.comentario,
            }
            for comentario in comentarios
        ]

        return JsonResponse({'data': comentarios_data})

class ModificarComentarioView(View):
    def post(self, request, comentario_id):
        comentario = get_object_or_404(Comentario, id=comentario_id, usuario=request.user)
        nuevo_comentario = request.POST.get('comentario')
        if nuevo_comentario:
            comentario.comentario = nuevo_comentario
            comentario.save()
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error', 'mensaje': 'El comentario no puede estar vacío.'})

class EliminarComentarioView(View):
    def post(self, request, comentario_id):
        comentario = get_object_or_404(Comentario, id=comentario_id, usuario=request.user)
        comentario.delete()
        return JsonResponse({'status': 'success'})