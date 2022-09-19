import pandas as pd
import numpy as np
from os import path


actualPath = path.dirname(__file__)
dataFile = path.join(actualPath, 'data', 'processed', 'df_desnorm.csv')

df = pd.read_csv(dataFile, sep=';')


# PUNTO 3

# A. ¿Cuántas tracks hay del artista Radiohead?



def point_3a(artist_count):
    """Function to return how many tracks there are by a given artist

    Args:
        artist_count (str): Type the artist name
    """

    point_3A = len(df[df['name_artist'] == artist_count.title()])
    print(f'El dataset contiene {point_3A} canciones de\
    {artist_count.title()}\n')


point_3a('Radiohead')

# B. ¿Cuántas tracks contienen la palabra ‘police’ en el título?


def point_3B(contain_in_title):
    """Function to return how many tracks contain a certain word,
    regardless of whether it is upper or lower case.
    Case insensitive

    Args:
        contain_in_title (str): any single word
    """

    point_3B = len(df[
        df['name_track'].str.contains(contain_in_title, case=False)])
    print(f'El dataset contiene {point_3B} titulos con la palabra:\
    {contain_in_title}\n')


point_3B('police')

# C. ¿Cuántas tracks son de álbumes publicados en la década del 1990?


def point_3C(decade):
    """Function to return how many tracks are from albums
    released in any particular decade.

    Args:
        decade (int): Type two last digits from any decade of the XX century
    """

    point_3C = len(df[
        (df['release_year'] >= int('19'+str(decade))) &
        (df['release_year'] < int('19'+str(decade+10)))])
    print(f"El dataset contiene {point_3C} titulos\
    de la decada del '{decade}\n")


point_3C(90)

# D. ¿Cuál es la track con más popularidad de los últimos 10 años?


def point_3D(years):
    """Function to return what is the most popular track of the last X years

    Args:
        years (int): Type the number of years as an integer
        to perform the calculation
    """

    point_3Da = df[
        'name_track'][df['release_year'] >= (
            int('2021') - int(years))].max()
    point_3Db = df[
        'popularity_track'][df['release_year'] >= (
            int('2021') - int(years))].max()

    print(f"El track con mayor popularity de los ultimos {years} años\
    es {point_3Da} y tiene una popularidad de {point_3Db}\n")


point_3D(10)

# E. ¿Qué artistas tienen tracks en cada una de las décadas desde el 1960?


def artists_all_decades(data):
    """Function that returns function that returns how many artists
    (and who they are) with tracks in each of the decades since the 1960s.

    Args:
        data (dataframe): enter the dataframe analysed
    """
    data['decade_group'] = np.where(
        (data['release_year'] >= 1960) & (
            data['release_year'] < 1970), '60',
        np.where((data['release_year'] >= 1970) & (
            data['release_year'] < 1980), '70',
            np.where((data['release_year'] >= 1980) & (
                data['release_year'] < 1990), '80',
            np.where((data['release_year'] >= 1990) & (
                data['release_year'] < 2000), '90',
                np.where((data['release_year'] >= 2000) & (
                    data['release_year'] < 2010), '2000',
                np.where((data['release_year'] >= 2010) & (
                    data['release_year'] < 2020), '2010',
                    np.where((data['release_year'] >= 2020) & (
                        data['release_year'] < 2030), '2020',
                    '50 o menor')))))))

    df2_denorm = data[['name_artist', 'decade_group']].drop_duplicates()
    df3 = df2_denorm.pivot(index=['name_artist'], columns='decade_group',
                           values='decade_group')

    df3['decade_check'] = np.where(
        df3['60'].notnull() & df3['70'].notnull() & df3['80'].notnull() &
        df3['90'].notnull() & df3['2000'].notnull() & df3['2010'].notnull() &
        df3['2020'].notnull(), 'ok', '')
    draft = df3[df3['decade_check'] == 'ok']
    all_decades = draft.reset_index()
    all_decades_from1960 = all_decades['name_artist'].to_list()

    print(f'Los artistas que tienen al menos un album hasta hoy en cada decada\
    desde 1960 son {len(all_decades_from1960)}, estos son:')

    for i in all_decades_from1960:
        print(i)
    print()


artists_all_decades(df)

