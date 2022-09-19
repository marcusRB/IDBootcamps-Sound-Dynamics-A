# Tarea 8: Llamadas a API externa
# Francesco Esposito - Febrero 2022

import time
import grequests
import pandas as pd
from os import path
from utility import countryCodes


def get_artists_data_async(artistsList, verbose=False):
    endPoint = 'https://theaudiodb.com/api/v1/json/2/search.php?s='
    df = pd.DataFrame(columns=['artist_name', 'formed_year', 'country'])
    addedCount = notFoundCount = 0
    urls = [endPoint + e for e in artistsList]
    rs = (grequests.get(u) for u in urls)
    responses = grequests.map(rs)
    for i, response in enumerate(responses):
        if response.status_code == 200:
            response = response.json()
            if response['artists'] is not None:
                addedCount += 1
                if response['artists'][0]['strCountryCode'] == "":
                    country = 'Unknown'
                else:
                    country = response['artists'][0]['strCountryCode']
                    country = countryCodes.ISO3166[country]
                    formYear = response['artists'][0]['intFormedYear']
                newLine = {'artist_name': artistsList[i].title(),
                           'formed_year': formYear,
                           'country': country}
                df = df.append(newLine, ignore_index=True)
                if verbose:
                    print(f'Nuevo artista añadido: {artistsList[i].title()}')
            else:
                if verbose:
                    print(f'Artista {artistsList[i].title()} no encontrado')
                notFoundCount += 1
        else:
            print('La llamada al endpoint no ha dado éxito positivo')
    if verbose:
        print(f'Artistas añadidos: {addedCount}\n\
        Artistas no encontrados: {notFoundCount}')
    return df


if __name__ == '__main__':
    # # Mostrar por pantalla los datos obtenidos
    # (artist_name, formed_year, country)
    # # para los artistas Radiohead, David Bowie y Måneskin.
    artists = ['Radiohead', 'David Bowie', 'Måneskin']
    print(get_artists_data_async(artists))

    # Evaluad vuestra implementación descargando la información de todos los
    # artistas del dataset original y comentad brevemente por qué creéis que
    # vuestra implementación es eficiente y cómo creéis que escalará si se
    # tienen que buscar miles de artistas simultáneamente.
    actualPath = path.dirname(__file__)
    filePath = path.join(actualPath, 'data', 'raw', 'artists_norm.csv')
    exportFile = path.join(actualPath,
                           'data',
                           'processed',
                           'artists_audiodb.csv')
    artistsDF = pd.read_csv(filePath, sep=';')
    artists = list(artistsDF['name'])
    start = time.time()
    df = get_artists_data_async(artists)
    end = time.time() - start
    print(end, 'seconds')
    df.to_csv(exportFile, sep=';', index=False)

'''
En ésta tarea el objetivo es crear un dataset con datos sacados de la API de
AudioDB. Según la documentación de la web, se pide hacer como mucho una llamada
cada 2 segundos. De ésta manera, independientemente de la eficiencia del script
no podremos llamar más de 30 endpoint por minuto.
Si no tenemos en cuenta ésta limitación y teniendo en cuenta que el servicio
nos lo permite, ya podríamos llamar unos 450/500 endpoint por minuto, que no
está tan mal.
Aún así he ido más allá y he encontrado una manera más eficiente de hacerlo,
utilizando una librería, grequests, que nos permite hacer llamadas a APIs de
manera asíncrona. Implementando el uso de esa librería, he obtenido unos
resultados mejores, llegando a poder llamar aproximativamente 3600 endpoint
por minuto, dependiendo de distintos factores.
En conclusión, creo que mi implementación es eficiente y podría ejecutar la
tarea con muchos más artistas en tiempos razonables.
'''
