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


actualPath = path.dirname(__file__)
dataFile = path.join(actualPath, 'data', 'processed', 'df_desnorm.csv')

df = pd.read_csv(dataFile, sep=';')


# Tarea 7: Calcular similitud entre artistas


df['loudness'] = df['loudness'].apply(lambda x: x * -1)
df['loudness']

audio_features = ['danceability', 'energy', 'key', 'loudness',
                  'mode', 'speechiness', 'acousticness', 'instrumentalness',
                  'liveness', 'valence', 'tempo', 'time_signature']

df_af = df.groupby('name_artist')[audio_features].mean().reset_index()


scaler = MinMaxScaler()
df_af[audio_features] = scaler.fit_transform(df_af[audio_features])

df7a = df_af.set_index('name_artist')


artist_filter = ['Metallica', 'Extremoduro', 'Ac/Dc', 'Hans Zimmer']

df7c = df7a[df7a.index.isin(artist_filter)]


def similarities(artists, method, showPlot=True):

    calculus1 = 1/(1+squareform(pdist(df7c, metric=method)))
    calculus2 = pd.DataFrame(calculus1, columns=artists, index=artists)
    print(f"Las similitudes entre los artistias seleccionados son:\n\n\
{calculus2}")
    cmap = sns.light_palette("seagreen", as_cmap=True)
    sns.heatmap((calculus2), cmap=cmap, annot=True)
    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")
    plt.savefig(saveFile, dpi=300)
    if showPlot:
        plt.tight_layout()
        plt.show()


saveFile = path.join(path.dirname(__file__), 'graphics', 'tarea7Graphic.png')

if __name__ == '__main__':
    similarities(artist_filter, method='euclidean')
    similarities(artist_filter, method='cosine')
