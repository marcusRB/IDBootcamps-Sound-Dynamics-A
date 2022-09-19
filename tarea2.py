# Tarea 2: Explorar alternativas de lectura de ficheros
# Francesco Esposito - Febrero 2022

# Vamos a importar las librerías necesarias para ésta comparativa
from os import path
import time
import pandas
import polars
import csv
import matplotlib.pyplot as plt
import seaborn as sns

# Definimos las funciones para leer una columna de un dataframe y
# devolverla en una lista


def get_column_pandas(filePath, column):
    '''
    Una función para leer los valores de una columna usando el módulo Pandas

    Args:
        filePath (string): la ruta del archivo CSV a leer
        column (string): nombre de la columna del archivo CSV que queremos leer

    Returns:
        list: una lista con todos los valores de la columna
    '''
    df = pandas.read_csv(filePath, sep=';')
    return list(df[column])


def get_column_polars(filePath, column):
    '''
    Una función para leer los valores de una columna usando el módulo Polars
    Ese módulo promete ser mucho más rápido que Pandas porque aprovecha
    la potencia de cálculo de todos los nucleos de la CPU

    Args:
        filePath (string): la ruta del archivo CSV a leer
        column (string): nombre de la columna del archivo CSV que queremos leer

    Returns:
        list: una lista con todos los valores de la columna
    '''
    df = polars.read_csv(filePath, sep=';')
    return list(df[column])


def get_column_csv(filePath, column):
    '''
    Una función para leer los valores de una columna
    usando el módulo CSV integrado en Python

    Args:
        filePath (string): la ruta del archivo CSV a leer
        column (string): nombre de la columna del archivo CSV que queremos leer

    Returns:
        list: una lista con todos los valores de la columna
    '''
    with open(filePath, 'r', newline='', encoding='utf-8') as f:
        df = csv.reader(f, delimiter=';')
        header = df.__next__()
        c = header.index(column)
        return [line[c] for line in df]


def get_column_list(filePath, column):
    '''
    Una función para leer los valores de una columna sin usar ninguna librería
    Simplemente utiliza la función Open y List Comprehension de Python

    Args:
        filePath (string): la ruta del archivo CSV a leer
        column (string): nombre de la columna del archivo CSV que queremos leer

    Returns:
        list: una lista con todos los valores de la columna
    '''
    with open(filePath, 'r', encoding='utf-8') as f:
        list = [line[:-1].split(';') for line in f]
    c = list[0].index(column)
    return [elem[c]for elem in list][1:]


def exec_time(dataPath, files, columns, rep):
    '''
    Una función que permite medir el tiempo medio de ejecución de todas
    las funciones sobre todos los fichero dado un número de repeticiones

    Args:
        dataPath (str): la ruta donde se encuentran los ficheros
        files (list): una lista con los nombres de los ficheros que utilizar
        columns (list): una lista con el nombre de la columna a leer
                        para cada fichero
        rep (int): un entero con el número de veces que hay que llamar
                   cada función para poder sacar un promedio

    Returns:
        list: una lista con media tiempo de lectura y número de lineas leídas
        para todos los ficheros y funciones
    '''
    # Medimos el tiempo de ejecución de todos los ficheros
    # con todas las funciones
    functions = ['get_column_pandas',
                 'get_column_polars',
                 'get_column_csv',
                 'get_column_list']
    result = [[[], []], [[], []], [[], []], [[], []]]
    for i in range(len(files)):
        file = path.join(dataPath, files[i])
        col = columns[i]
        exTimes = [[], [], [], []]
        for i, fun in enumerate(functions):
            for n in range(rep):
                start = time.time()
                functionReturn = globals()[fun](file, col)
                # functionReturn = eval(fun + '(file, col)') # Alternativa
                exTimes[i].append(time.time() - start)
                if n == 0:
                    result[i][0].append(len(functionReturn))
            # Calculo el promedio del tiempo de ejecución para cada file
            result[i][1].append((sum(exTimes[i])/rep)*1000)
    return result


def draw_plot(data, saveFile, showPlot=False):
    '''
    Una función que permite dibujar un gráfico con la
    comparativa entre las diferentes funciones

    Args:
        data (list): la lista generada con la función exec_time().
                     Ésta lista comprende 4 listas, una para cada función.
                     Cada lista de función comprende otras dos listas:
                     - Una con el número de lineas leídas para cada fichero;
                     - Otra con la media del tiempo empleado para cada fichero.
        saveFile (str): la ruta absoluta en donde guardar la imagen del gráfico

    '''
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    for x in range(len(data)):
        ax = sns.lineplot(x=data[x][0], y=data[x][1], color=colors[x])
        plt.text(data[x][0][-1]+100, data[x][1][-1],
                 f'{int(data[x][1][-1])}ms',
                 color=colors[x])
    ax.set_title(f'Comparativa de eficiencia entre 4 distintos\n\
métodos para leer una columna de un archivo CSV')
    ax.set(xlabel='Cantidad de filas leídas',
           ylabel=f'Media tiempo de ejecución (ms) para {rep} repeticiones')
    plt.legend(labels=[f'Pandas {pandas.__version__}',
                       f'Polars {polars.__version__}',
                       'Python CSV',
                       'List Comprehension'])
    plt.grid()
    # Configura la ventana maximizada dedependiendo del backend
    # https://matplotlib.org/stable/users/explain/backends.html
    figManager = plt.get_current_fig_manager()
    if plt.get_backend() == 'QtAgg':
        figManager.window.showMaximized()
    elif plt.get_backend() == 'TkAgg':
        figManager.window.state('zoomed')
    elif plt.get_backend() == 'wxAgg':
        figManager.frame.Maximize(True)
    else:
        print('Imposible maximizar la ventana de la gráfica')
    figManager.canvas.manager.set_window_title('Comparativa de eficiencia')
    plt.savefig(saveFile, dpi=300)
    if showPlot:
        plt.show()


###############################################################################
# Definimos los archivos, columnas con las que trabajar y las repeticiones

saveFile = path.join(path.dirname(__file__), 'graphics', 'tarea2Graphic.png')
dataPath = path.join(path.dirname(__file__), 'data', 'raw')
files = ['artists_norm.csv', 'albums_norm.csv', 'tracks_norm.csv']
columns = ['artist_id', 'album_id', 'track_id']
rep = 10  # Veces que hay que llamar cada función

if __name__ == '__main__':
    print('Script starts')
    print('Calculando el tiempo de ejecución')
    start = time.time()
    d = exec_time(dataPath, files, columns, rep)
    end = time.time()
    print(f'Tiempo empleado para {rep} repeticiones: \
{int(end - start)} segundos')
    print('Dibujando el gráfico')
    draw_plot(d, saveFile, showPlot=True)
