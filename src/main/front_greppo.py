from greppo import app
import geopandas as gpd
import pandas
import json
import sys
sys.path.insert(1, './')
import wrapper_twitter as Twitter
#Creo un wrapper, que nos hara falta despues para las consultas
twitter = Twitter.wrapper_twitter()

app.base_layer(
    name="Open Street Map",
    visible=True,
    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
    subdomains=None,
    attribution='(C) OpenStreetMap contributors',
)

app.map(center=[40.4165,-3.70256], zoom=6)

text_1 = """
# Bienvenido a InfoGe
## Herramienta para obtener estadísticas de Twitter con Localizaciones!
### Haga una búsqueda de las comunidades para ver en el mapa la provincia con más interes.
"""

app.display(name='text-1', value=text_1)

#Carga los datos de comunidades y provincias
geodatos_comunidades = gpd.read_file("./comunidades.json")
geodatos_provincias = gpd.read_file("./provincias.json")

comunidades = list(set(list(geodatos_comunidades.Comunidad)))#crea una lista con las comunidades
comunidades.sort()#Orden alfabetico que sea mas facil encontrar
comunidades.insert(0,"")#metemos un vacio por si no se quiere seleccionar comunidad

selector_comunidad = app.select(name="Selecciona una comunidad", options=comunidades, default="")

if selector_comunidad!='':
    filtrado = geodatos_comunidades[geodatos_comunidades.Comunidad == selector_comunidad]
    app.vector_layer(data = filtrado,name = "Comunidad",description = "Resaltado de Comunidad Seleccionada" ,style = {"color": "#000000", "fillColor":"#4daf4a","fillOpacity":"0.1"},) 
    
    
    f = open('./provincias.json',)
    provincias_json = json.load(f)
    provincias_comunidad = list()
    for i in range(52):
        comunidad_p = provincias_json['features'][i]['properties']['Comunidad']
        tmp = comunidad_p.replace(' ','')
        
        tmp2 = selector_comunidad.replace(' ','')

        if tmp.lower() in tmp2.lower():
            provincias_comunidad.insert(0,provincias_json['features'][i]['properties']['provincia'])
    
    

    hot_provincia = twitter.getLocalizacionesCalientes(provincias_comunidad)
    
    if hot_provincia != []:
        #pueblos_geo = filtrado[filtrado.Comunidad.isin(provincias_comunidad)]#con esto filtramos los pueblos que no tienen temas calientes,
        #hay que sustituir la lista por la lista que devuelva el metodo del wrapper si se llega a hacer, si no pues con todos los pueblos
        centroides = geodatos_provincias[geodatos_provincias.provincia == hot_provincia[0]].centroid #esto saca una lista de los puntos centrales, pero los deja sin nombre ni datos
        #para eso convertimos nuevamente a geodataframe estos puntos y le metemos las columnas necesarias
        gdf_centroides = gpd.GeoDataFrame(centroides, geometry=0)
        #ahora que ya tenemos los puntos formados con su informacion pertinente lo dibujamos en el mapa
        puntos_calientes = app.vector_layer(name="Puntos Calientes", data=gdf_centroides, description="Puntos calientes y su motivo", style= {"color":"#e41a1c","weight":"3"}, visible=True)
        
        text_h = """
# Provincia con más Interés : """
        app.display(name='text-1', value=text_h)

        text_h = """
#🔥 """ + hot_provincia[0] + """ 🔥"""
        app.display(name='text-1', value=text_h)

    
text_2 = """ ------------ """
app.display(name='text-2', value=text_2)

text_1 = """
### Rellene los parametros para obtener estadísticas sobre Comunidades, Provincias o incluso Pueblos. 
"""

app.display(name='text-1', value=text_1)

texto_provincia = app.text(value='', name='Introduce el Nombre de una Comunidad, Provincia o Pueblo.')

selector_estadisticas = app.select(name="Tipo de Estadísticas", options=["Diaria","General"], default="General")

if texto_provincia!='':
    text_2 = """
# Trending Topic
## Lista de temas más hablados
"""
    app.display(name='text-2', value=text_2)

    temas_provincia = twitter.getTemasCalientes(texto_provincia)
    for tmp in temas_provincia:
        text_3 = '🔥 ' + tmp 
        app.display(name='text-3', value=text_3)

    diaria = False
    if selector_estadisticas=="Diaria":
        diaria = True
    
    cuentas_provincia = twitter.getCuentas(texto_provincia)
    likes = 0
    retweets = 0
    vistas = 0
    busquedas = 0
    seguidores = 0
    cantidad_tweets = 0
    for tmp in cuentas_provincia:       
        likes += twitter.getLikesUsuario(tmp,diaria)
        retweets += twitter.getRetweetsUsuario(tmp,diaria)
        vistas += twitter.getVistasUsuario(tmp,diaria)
        seguidores += twitter.getFollowersUsuario(tmp)
        cantidad_tweets += twitter.getCantidadTweetsUsuarios(tmp,diaria)     
    busquedas += twitter.getBusquedas(texto_provincia,diaria)


    text_4 = """
# Estadísticas """
    app.display(name='text-2', value=text_4)

    text_4 = """
## Likes: """ + str(likes)
    app.display(name='text-2', value=text_4)

    text_4 = """
## Retweets: """ + str(retweets)
    app.display(name='text-2', value=text_4)

    text_4 = """
## Vistas: """ + str(vistas)
    app.display(name='text-2', value=text_4)

    text_4 = """
## Busquedas: """ + str(busquedas)
    app.display(name='text-2', value=text_4)

    text_4 = """
## Seguidores: """ + str(seguidores)
    app.display(name='text-2', value=text_4)

    text_4 = """
## Cantidad de Tweets: """ + str(cantidad_tweets)
    app.display(name='text-2', value=text_4)

    app.bar_chart(
        name="Gráfica de Estadísticas",
        x = ['Likes', 'Retweets', 'Vistas', 'Busquedas','Seguidores','Tweets'],
        y=[likes, retweets, vistas, busquedas, seguidores, cantidad_tweets,],
        color="rgb(200, 50, 150)",
    )



