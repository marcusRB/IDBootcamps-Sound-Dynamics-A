import pandas as pd
import numpy as np
from os import path
import zipfile as zip
import seaborn as sns
import matplotlib.pyplot as plt
import time
import polars
import csv
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial.distance import pdist, squareform


datapath = 'data-8732680f-fcf7-49d8-a6fa-479cbe4aaa9c.zip'


def unzip(path):
    """Function to unzip a file from the current directory

    Args:
        path (str): file name to unzip

    Returns:
        list: list of unzipped files excluding those starting with '__MACOSX/'
    """
    # Primero comprobamos que le hemos pasado el path
    # de un archivo ZIP como parametro
    if zip.is_zipfile(path):
        # Luego creamos un objeto ZIP,
        # lo extraemos en la misma carpeta y devolvemos
        # una lista con el contenido del archivo (los files)
        with zip.ZipFile(path, 'r') as zipObj:
            # Extract all the contents of zip file in current directory
            zipObj.extractall()
            return [elem for elem in zipObj.namelist()
                    if not elem.startswith('__MACOSX/')]
    else:
        print(f'{path} no es un fichero comprimido')


unzip(datapath)


# Cargamos los archivos


def read_files(files):
    """Function to read files from a current path and
    measure the row and column size of each one

    Args:
        files (list): List of files
    """
    actualPath = path.abspath('')
    df = []
    for i in files:
        df.append(pd.read_csv(path.join(actualPath, i), sep=';'))
    j = 0
    for w in df:
        j += 1
        print(f'El file {j} contiene {len(w)} filas y {len(w.columns)} \
columnas\n')


read_files(unzip(datapath))


def create_df1():
    """Function to create a dataframe on the global memory
    from an individual CSV file
    """
    global dataset1
    actualPath = path.abspath('')
    dataset1 = pd.read_csv(path.join(actualPath, 'tracks_norm.csv'), sep=';')


df1 = create_df1()


def create_df2():
    """Function to create a dataframe on the global memory
    from an individual CSV file
    """
    global dataset2
    actualPath = path.abspath('')
    dataset2 = pd.read_csv(path.join(actualPath, 'albums_norm.csv'), sep=';')


df2 = create_df2()


def create_df3():
    """Function to create a dataframe on the global memory
    from an individual CSV file
    """

    global dataset3
    actualPath = path.abspath('')
    dataset3 = pd.read_csv(path.join(actualPath, 'artists_norm.csv'), sep=';')


df3 = create_df3()

album_artist_desnorm = pd.merge(dataset2, dataset3, on='artist_id', how='left')

df_denorm = pd.merge(dataset1, album_artist_desnorm,
                     on=['artist_id', 'album_id'], how='left')

df_denorm.rename(columns={'name': 'name_track',
                          'popularity': 'popularity_track',
                          'name_x': 'name_album',
                          'popularity_x': 'popularity_album',
                          'name_y': 'name_artist',
                          'popularity_y': 'popularity_artist'},
                 inplace=True)

df_denorm['name_artist'] = df_denorm['name_artist'].str.title()

print(f"Se llenaran {df_denorm['popularity_track'].isna().sum()} \
con el promedio de los valores existentes en la columna 'popularity_track'\n")

df_denorm['popularity_track'] = df_denorm['popularity_track'].fillna(
    (df_denorm['popularity_track'].mean()))

print(f"La columna Popularity_track ahora tiene \
{df_denorm['popularity_track'].isna().sum()} valores NA dado que se han \
llenado con el promedio de la columna\n")


# Tarea 7: Calcular similitud entre artistas


df_denorm['loudness'] = df_denorm['loudness'].apply(lambda x: x * -1)
df_denorm['loudness']

audio_features = ['danceability', 'energy', 'key', 'loudness',
                  'mode', 'speechiness', 'acousticness', 'instrumentalness',
                  'liveness', 'valence', 'tempo', 'time_signature']

df_af = df_denorm.groupby('name_artist')[audio_features].mean().reset_index()


scaler = MinMaxScaler()
df_af[audio_features] = scaler.fit_transform(df_af[audio_features])

df7a = df_af.set_index('name_artist')


artist_filter = ['Metallica', 'Extremoduro', 'Ac/Dc', 'Hans Zimmer']

df7c = df7a[df7a.index.isin(artist_filter)]


def similarities(artists, method):

    calculus1 = 1/(1+squareform(pdist(df7c, metric=method)))
    calculus2 = pd.DataFrame(calculus1, columns=artists, index=artists)
    print(f"Las similitudes entre los artistias seleccionados son:\n\n\
{calculus2}")
    cmap = sns.light_palette("seagreen", as_cmap=True)
    sns.heatmap((calculus2), cmap=cmap, annot=True)
    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")
    plt.show()


if __name__ == '__main__':
    similarities(artist_filter, method='euclidean')
if __name__ == '__main__':
    similarities(artist_filter, method='cosine')
