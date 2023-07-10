import pandas as pd
import folium
import geopandas as gpd
import random

df = pd.read_csv("C:/Users/pydim/Desktop/MSPR2/Data/Data1.csv", sep=";", dtype=object)

# Convertir la colonne "Voix" en type numérique
df['Voix'] = pd.to_numeric(df['Voix'], errors='coerce')

# Regroupement des voix
df = df.loc[df.groupby("Code de la commune")["Voix"].idxmax()]

participants = df['Nom'].unique()
colors = ['#%06x' % random.randint(0, 0xFFFFFF) for _ in range(len(participants))]
color_mapping = dict(zip(participants, colors))

# Carte
geojson_data = "https://france-geojson.gregoiredavid.fr/repo/regions/nouvelle-aquitaine/communes-nouvelle-aquitaine.geojson"
map_df = gpd.read_file(geojson_data)

# Mappage des votes avec les code departement
merged_df = map_df.merge(df, how="inner", left_on="code", right_on="Code de la commune")

# zoom sur la carte
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
        fields=['Nom', 'Libellé de la commune'],
        aliases=['Nom', 'Commune'],
        labels=True,
        sticky=True
    )
).add_to(m)

m.save("map.html")
