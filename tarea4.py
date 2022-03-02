import pandas as pd
import numpy as np
from os import path
import zipfile as zip
import seaborn as sns
import matplotlib.pyplot as plt

actualPath = path.dirname(__file__)
dataFile = path.join(actualPath, 'data', 'processed', 'df_desnorm.csv')

df = pd.read_csv(dataFile, sep=';')

# PUNTO 4

# A. Calcular el mínimo, la media y el máximo de la feature energy
# de todas las tracks de Metallica.

def gauge_artist_energy(artist_name):
    """Function that calculate the minimum, average and maximum feature energy
    of all the tracks from any artist.

    Args:
        artist_name (str): Type the artist (case insensitive)
        to perform the calculation
    """

    point_4A1 = df[
        'energy'][df['name_artist'] == artist_name.title()].min()
    point_4A2 = df[
        'energy'][df['name_artist'] == artist_name.title()].max()
    point_4A3 = df[
        'energy'][df['name_artist'] == artist_name.title()].mean()
    print(f'Los tracks de {artist_name.title()} tienen una\
    energia minima de {round(point_4A1,2)}, \n\
    energia maxima de {round(point_4A2,2)}, \n\
    energia promedio de {round(point_4A3,2)}\n')


gauge_artist_energy('Metallica')

# B. Calcular la media de la feature danceability de cada álbum de Coldplay
# y crear una gráfica para visualizar el resultado.


def danceability(artist_name, showPlot=True):
    """Function that returns a graph with the average danceability
    of each album from any given artist.

    Args:
        artist_name (str): Type the artist (case insensitive)
        to perform the graph
    """

    point_4B = df[['name_album', 'danceability']][df[
        'name_artist'] == artist_name.title()].groupby(
            'name_album').mean().reset_index()
    sns.barplot(x="danceability", y="name_album", data=point_4B,
                palette='rocket',
                order=point_4B.sort_values('danceability',
                                           ascending=False).name_album)
    print('Please look at the screen to check\
    that the graph has been displayed.\n')
    plt.savefig(saveFile, dpi=300)
    if showPlot:
        plt.tight_layout()
        plt.show()

saveFile = path.join(path.dirname(__file__), 'graphics', 'tarea4Graphic.png')


danceability('Coldplay')
