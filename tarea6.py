# Tarea 6: Comparar artistas visualmente
# Francesco Esposito - Febrero 2022

from os import path
from utility import spotify
from matplotlib import pyplot as plt
import pandas as pd


def artists_compare(dataframePath,
                    audioFeature,
                    artists,
                    saveFile,
                    showPlot=False):
    '''
    Función para comparar las audio features de dos artistas

    Args:
        dataframePath (str): La ruta donde se encuntra il dataframe de Spostify
        audioFeature (str): La audio feature que se quiere comparar
        artists (list): Una lista con los nombres de los artistas a comparar
                        Se aceptan entre 2 y 5 nombres que deben ser "string"
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
    # Comprueba si los artistas están en el dataframe
    artists = [artist.title() for artist in artists]
    for artist in artists:
        if artist not in df['name_artist'].unique().tolist():
            print(f'El artista "{artist}" no está en el dataframe')
            return
    # Crea una lista con los audio features de los artistas y dibuja el gráfico
    data = [df[audioFeature][df.name_artist == artist] for artist in artists]
    if len(artists) < 2:
        print('Para la comparativa hacen falta al menos 2 artistas')
        return
    elif len(artists) == 2:
        h1 = plt.hist(data[0],
                      alpha=0.5,
                      bins=8,
                      density=True,
                      edgecolor="black",
                      color='red',
                      label=artists[0])
        plt.hist(data[1],
                 alpha=0.5,
                 bins=h1[1],
                 density=True,
                 edgecolor="black",
                 color='blue',
                 label=artists[1])
    elif 2 < len(artists) < 6:
        plt.hist(data, bins=8, label=artists, density=True)
    elif len(artists) >= 6:
        print('No se pueden comparar más de 5 artistas')
        return
    title = 'Comparativa audio features entre artistas'
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
    savePath = path.join(actualPath, 'graphics', 'tarea6Graphic.png')
    feature = 'energy'
    artistas = ['Adele', 'Extremoduro']
    artists_compare(dataPath, feature, artistas, savePath, showPlot=False)
