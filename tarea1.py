# Tarea 1: Crear dataset de tracks des-normalizado
# Francesco Esposito - Febrero 2022

import zipfile as zip
from os import path
import pandas as pd


def unzip(dataFile):
    '''
    Función para descomprimir un fichero .zip y devolver una lista con los
    nombres de los ficheros contenidos

    Args:
        path (str): La ruta del fichero comprimido (.zip)

    Returns:
        list: una lista con los nombres de los ficheros descomprimidos
    '''
    # Comprobamos que le hemos pasado el path de un archivo ZIP como parametro
    if zip.is_zipfile(dataFile):
        savePath = path.split(dataFile)[0]
        # Creamos un objeto ZIP, lo extraemos en la misma carpeta y devolvemos
        # una lista con el contenido del archivo (los files)
        with zip.ZipFile(dataFile, 'r') as zipObj:
            zipObj.extractall(savePath)
            return [path.join(savePath, elem) for elem in zipObj.namelist()
                    if not elem.startswith('__MACOSX/')]
    else:
        print(f'{dataFile} no es un fichero comprimido')
        return False


def denormalize(dataframesNames):
    '''
    Función para desnormalizar dataframes del proyecto:
    IDBootcamps Sound Dynamics

    Args:
        dataframesNames (list): una lista con los nombres de los dataframes
        contenidos en el fichero ZIP

    Returns:
        pandas.core.frame.DataFrame: un único dataframe desnormalizado
    '''

    if dataframesNames is not False:
        dataframes = []
        for e in dataframesNames:
            dataframes.append(pd.read_csv(
                path.join(actualPath, 'data', 'raw', e),
                sep=';'))
        album_artist_desnorm = pd.merge(dataframes[0], dataframes[1],
                                        on='artist_id', how='left')
        df_denorm = pd.merge(dataframes[2],
                             album_artist_desnorm, on=['artist_id',
                                                       'album_id'],
                             how='left')
        # Renombramos los campos del DF desnormalizado
        df_denorm.rename(columns={'name': 'name_track',
                                  'popularity': 'popularity_track',
                                  'name_x': 'name_album',
                                  'popularity_x': 'popularity_album',
                                  'name_y': 'name_artist',
                                  'popularity_y': 'popularity_artist'},
                         inplace=True)
        # Corregimos los nombres de los artistas
        df_denorm['name_artist'] = df_denorm['name_artist'].str.title()
        # Corregimos los valores de 'popularity' que no tienen valor
        nanCount = df_denorm['popularity_track'].isna().sum()
        df_denorm['popularity_track'] = df_denorm['popularity_track'].fillna(
            (df_denorm['popularity_track'].mean()))
        print(f'El dataset final contiene {df_denorm.shape[0]} filas y \
{len(df_denorm.columns)} columnas')
        print(f"Número de track que no tenían un valor de 'popularity': \
{nanCount}")
        return df_denorm
    else:
        print('Imposible desnormalizar el dataframe')


if __name__ == '__main__':
    actualPath = path.dirname(__file__)
    dataFile = path.join(actualPath, 'data', 'raw', 'data.zip')
    df = denormalize(unzip(dataFile))
    saveFile = path.join(actualPath, 'data', 'processed', 'df_desnorm.csv')
    df.to_csv(saveFile, sep=';', index=False)
