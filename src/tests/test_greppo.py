from greppo import app
import geopandas as gpd

app.display(name='title', value='Vector demo')
app.display(name='description',
            value='A Greppo demo app for vector data using GeoJSON data.')
app.map(center=[40.4165,-3.70256], zoom=6)#con app.map se puede ajustar el zoom y la ubicación de partida

app.base_layer(
    name="Open Street Map",
    visible=True,
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    subdomains=None,
    attribution='(C) OpenStreetMap contributors',
)
app.map(center=[40.4165,-3.70256], zoom=6)#con app.map se puede ajustar el zoom y la ubicación de partida

data_gdf = gpd.read_file("./src/tests/geodatos.json")
filtrado = data_gdf[data_gdf.provincia == "Ciudad Real"]

app.vector_layer(
    data = filtrado,
    name = "Prov",
    description = "Provincias de españa",
    style = {"color": "#000000", "fillOpacity":"0"},
)

puntitos = filtrado.centroid
puntitos_vector = app.vector_layer(name="puntos",data=puntitos,description="puntos calientes", style= {"color":"#e41a1c"}, visible=True)

text_1 = """
## About the web-app

para realizar consultas introduce los datos y haz click en reevaluate para cargar
"""

app.display(name='text-1', value=text_1)

in_texto = app.text(name="Introduce la población:", value="")
select1 = app.select(name="First selector", options=["a", "b", "c"], default="a")
if in_texto != "":
    texto = "Has escrito "+in_texto
    app.display(name="prueba", value=texto)
if select1 =="a":
    app.display(name="", value="has seleccionado a")
if select1 =="b":
    app.display(name="", value="has seleccionado b")
    in_texto = app.text(name="Seleccion de b", value="")

for nombre in filtrado.poblacion:
    app.display(name="pobls",value=nombre)