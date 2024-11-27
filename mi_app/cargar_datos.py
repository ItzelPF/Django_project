import csv
from mi_app.models import Autor, Libro

def cargar_datos_csv(file_path):
    # Abrir el archivo y manejar el marcador BOM
    with open(file_path, 'r', encoding='utf-8-sig') as file:  # utf-8-sig elimina el BOM
        reader = csv.DictReader(file)
        columnas = reader.fieldnames  # Obtener nombres de las columnas
        print("Columnas detectadas en el CSV:", columnas)

        # Validar que las columnas requeridas existan
        required_columns = ['Titulo','Autor','Editorial','Año','ISBN']
        for col in required_columns:
            if col not in columnas:
                raise KeyError(f"Columna requerida no encontrada: {col}")

        # Procesar los datos
        for row in reader:
            # Crear o buscar el autor
            autor_nombre = row['Autor'].strip()
            autor, created = Autor.objects.get_or_create(nombre=autor_nombre)

            # Crear el libro
            Libro.objects.create(
                titulo=row['Titulo'].strip(),
                autor=autor,
                editorial=row['Editorial'].strip(),
                anio=int(row['Año']),
                isbn=row['ISBN'].strip()
            )
    print("Datos cargados correctamente.")