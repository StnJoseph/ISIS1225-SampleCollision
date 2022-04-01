"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """
import time
import tracemalloc
import config as cf
import model
import csv


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""


def newController():
    """
    Crea una instancia del modelo
    """
    control = {
        'model': None
    }
    control['model'] = model.newCatalog()
    return control


# Funciones para la carga de datos


def loadData(ctrlr):
    """
    Carga los datos de los archivos y cargar los datos en la
    estructura de datos
    """
    # inicializa el proceso para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()

    loadBooks(ctrlr)
    loadTags(ctrlr)
    loadBooksTags(ctrlr)

    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()
    # finaliza el proceso para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)

    return delta_time, delta_memory


def loadBooks(ctrlr):
    """
    Carga los libros del archivo. Por cada libro se indica al
    modelo que debe adicionarlo al catalogo.
    """
    booksfile = cf.data_dir + 'GoodReads/books-small.csv'
    input_file = csv.DictReader(open(booksfile, encoding='utf-8'))
    for book in input_file:
        model.addBook(ctrlr['model'], book)


def loadTags(ctrlr):
    """
    Carga todos los tags del archivo e indica al modelo
    que los adicione al catalogo
    """
    tagsfile = cf.data_dir + 'GoodReads/tags.csv'
    input_file = csv.DictReader(open(tagsfile, encoding='utf-8'))
    for tag in input_file:
        model.addTag(ctrlr['model'], tag)


def loadBooksTags(ctrlr):
    """
    Carga la información que asocia tags con libros en el catalogo
    """
    booktagsfile = cf.data_dir + 'GoodReads/book_tags-small.csv'
    input_file = csv.DictReader(open(booktagsfile, encoding='utf-8'))
    for booktag in input_file:
        model.addBookTag(ctrlr['model'], booktag)


# Funciones de consulta sobre el catálogo


def getBestBooks(ctrlr, number):
    """
    Retorna los mejores libros según su promedio
    """
    bestbooks = model.getBestBooks(ctrlr['model'], number)
    return bestbooks


def countBooksByTag(ctrlr, tag):
    """
    Retorna los libros que fueron etiquetados con el tag
    """
    return model.countBooksByTag(ctrlr['model'], tag)


def booksSize(ctrlr):
    """
    Numero de libros cargados al catalogo
    """
    return model.booksSize(ctrlr['model'])


def authorsSize(ctrlr):
    """
    Numero de autores cargados al catalogo
    """
    return model.authorsSize(ctrlr['model'])


def tagsSize(ctrlr):
    """
    Numero de tags cargados al catalogo
    """
    return model.tagsSize(ctrlr['model'])


def getBooksByAuthor(ctrlr, authorname):
    """
    Retorna los libros de un autor
    """
    authorinfo = model.getBooksByAuthor(ctrlr['model'], authorname)
    return authorinfo


def getBooksByTag(ctrlr, tagname):
    """
    Retorna los libros que han sido marcados con
    una etiqueta
    """
    books = model.getBooksByTag(ctrlr['model'], tagname)
    return books


def getBooksYear(ctrlr, year):
    """
    Retorna los libros que fueron publicados
    en un año
    """
    books = None
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()

    books = model.getBooksByYear(ctrlr['model'], year)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)

    return books, delta_time, delta_memory


def sortBooksByYear(ctrlr, year, fraction, rank):
    """
    Retorna los libros que fueron publicados
    en un año ordenados por rating
    """
    # respuesta por defecto
    books = None
    # inicializa el proceso para medir memoria
    tracemalloc.start()

    # toma de tiempo y memoria al inicio del proceso
    start_time = getTime()
    start_memory = getMemory()
    books = model.sortBooksByYear(ctrlr['model'], year, fraction, rank)

    # toma de tiempo y memoria al final del proceso
    stop_memory = getMemory()
    stop_time = getTime()
    # finaliza el procesos para medir memoria
    tracemalloc.stop()

    # calculando la diferencia de tiempo y memoria
    delta_time = deltaTime(stop_time, start_time)
    delta_memory = deltaMemory(stop_memory, start_memory)
    return books, delta_time, delta_memory

# Funciones para medir tiempos de ejecucion


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def deltaTime(end, start):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed


# Funciones para medir la memoria utilizada


def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(stop_memory, start_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
