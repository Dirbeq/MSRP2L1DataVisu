import pandas as pd
import folium
import geopandas as gpd
import random


def france():
    df = pd.read_csv("./dataset/Data2Clear.csv", sep=";", dtype=object, encoding='latin-1')
    df2 = pd.read_csv("./dataset/Data1Clear.csv", sep=";", dtype=object, encoding='latin-1')

    # Convertir la colonne "Voix" en type numérique
    df['Voix'] = pd.to_numeric(df['Voix'], errors='coerce')
    df2['Voix'] = pd.to_numeric(df['Voix'], errors='coerce')

    # Regroupement des voix
    df = df.loc[df.groupby("CodeDepartement")["Voix"].idxmax()]
    df2 = df2.loc[df.groupby("CodeDepartement")["Voix"].idxmax()]

    participants = df['Nom'].unique()
    colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(len(participants))]
    color_mapping = dict(zip(participants, colors))

    # On récupère les données géographiques
    geojson_data = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
    map_df = gpd.read_file(geojson_data)

    # Mappage des votes avec les codes de département
    merged_df = map_df.merge(df, how="inner", left_on="code", right_on="CodeDepartement")
    merged_df2 = map_df.merge(df2, how="inner", left_on="code", right_on="CodeDepartement")

    # Focus de la map sur une zone
    m = folium.Map(location=[46.678193, 1.81177], zoom_start=6)
    color_mapping = {
        "MÉLENCHON": "pink",
        "HIDALGO": "magenta",
        "DUPONT-AIGNAN": "green",
        "ARTHAUD": "orange",
        "PÉCRESSE": "cyan",
        "MACRON": "red",
        "LASSALLE": "teal",
        "POUTOU": "yellow",
        "LE PEN": "blue",
        "ZEMMOUR": "gray",
        "JADOT": "brown",
    }

    # Ajout des données de vote à la couche de géodonnées personnalisée avec couleurs aléatoires
    folium.GeoJson(
        merged_df,
        name='Votes par nom',
        style_function=lambda feature: {
            'fillColor': color_mapping.get(feature['properties']['Nom'], "gray"),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Nom', 'LibelleDepartement'],
            aliases=['Nom', 'Commune'],
            labels=True,
            sticky=True
        )
    ).add_to(m)

    m.save("map2.html")
    folium.GeoJson(
        merged_df2,
        name='Votes par nom',
        style_function=lambda feature: {
            'fillColor': color_mapping.get(feature['properties']['Nom'], "gray"),
            'color': 'black',
            'weight': 0.5,
            'fillOpacity': 0.7
        },
        tooltip=folium.features.GeoJsonTooltip(
            fields=['Nom', 'LibelleDepartement'],
            aliases=['Nom', 'Commune'],
            labels=True,
            sticky=True
        )
    ).add_to(m)

    m.save("map2_1.html")


if __name__ == "__main__":
    france()
