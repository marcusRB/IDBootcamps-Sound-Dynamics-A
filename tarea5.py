# Tarea 5: Histograma de una audio feature de un artista
# Francesco Esposito - Febrero 2022

from os import path
from utility import spotify
from matplotlib import pyplot as plt
import pandas as pd


def artist_visual_audiofeature(dataframePath,
                               audioFeature,
                               artist,
                               saveFile,
                               showPlot=False):
    '''
    Función para visualizar a través de un hístograma la feature de un artista

    Args:
        dataframePath (str): La ruta donde se encuntra il dataframe de Spostify
        audioFeature (str): La audio feature que se quiere mostrar
        artist (str): El nombre del artista
        saveFile (str): La ruta donde se quiere guardar el gráfico
        showPlot (bool, optional): Si es True, aparte de guardar el gráfico
                                   también se mostrará en pantalla.
                                   Por defecto es False.
    '''
    # Comprueba si el dataframe existe
    if path.isfile(dataframePath):
        df = pd.read_csv(dataframePath, sep=';')
    else:
        print(f'No se encuentra el archivo del dataframe:\n{dataframePath}')
        return
    # Comprueba si la audio feature pasada es correcta
    audioFeature = audioFeature.lower()
    if audioFeature not in spotify.audioFeatures:
        print(f'La audio feature {audioFeature} no es valida')
        print(f'Usa una de éstas: {spotify.audioFeatures}')
        return
    # Comprueba si el artista está en el dataframe
    artist = artist.title()
    if artist not in df['name_artist'].unique().tolist():
        print(f'El artista "{artist}" no está en el dataframe')
        return
    # Enseña la audio feature del artista en el gráfico
    data = df[audioFeature][df.name_artist == artist]
    plt.hist(data,
             bins=8,
             density=True,
             edgecolor="black",
             color='green',
             label=artist)

    title = f'Mostrando la audio feature {audioFeature} de {artist}'
    plt.title(title)
    plt.legend(loc='upper left')
    plt.xlabel(f'Audio feature: {audioFeature}')
    plt.ylabel('Density')
    try:
        plt.savefig(saveFile, dpi=300)
        print('Gráfico guardado correctamente en:')
        print(saveFile)
    except FileNotFoundError:
        print('Imposible guardar el gráfico porque la carpeta de destino \
no existe')
    if showPlot:
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
        figManager.canvas.manager.set_window_title(title)
        plt.show()


if __name__ == '__main__':
    actualPath = path.dirname(__file__)
    dataPath = path.join(actualPath, 'data', 'processed', 'df_desnorm.csv')
    savePath = path.join(actualPath, 'graphics', 'tarea5Graphic.png')
    feature = 'acousticness'
    artista = 'ed sheeran'
    artist_visual_audiofeature(dataPath, feature, artista, savePath)
