import geopandas as gpd
import pandas
import sys
sys.path.insert(1, './src/main')
import wrapper_twitter as Twitter
#Creo un wrapper, que nos hara falta despues para las consultas
twitter = Twitter.wrapper_twitter()


geodatos = gpd.read_file("geodatos.json")
provincias = list(set(list(geodatos.provincia)))#crea una lista con las provincias
provincias.sort()#Orden alfabetico que sea mas facil encontrar
provincias.insert(0,"")#metemos un vacio por si no se quiere seleccionar provincia
#creamos un selector con todas las provincias
selector_provincia="Ciudad Real"
if selector_provincia!='':#si hemos seleccionado una y le damos a recalculate se ejecuta esto
    filtrado = geodatos[geodatos.provincia == selector_provincia] #de todo el mapa sacamos los pueblos de la provincia
    #dibujamos en el mapa el contorno de los pueblos
    
    #sacamos la lista de pueblos de la provincia
    pueblos = list(set(list(filtrado.poblacion)))
    #llamo para que me devuevlan los pueblos mas calientes
    indexes = []
    nombres_poblaciones = []
    temas_calientes = []
    for pueblo in pueblos: #para ralentizar menos en vez de coger todos se podrían coger 10 al azar o de alguna forma en wrapper filtrar esta lista
        #rellena en forma de id del pueblo, nombre y array de temas para luego poner los puntos calientes
        try:
            temas_temp = twitter.getTemasCalientes(pueblo)
            indexes.append(filtrado[filtrado.poblacion==pueblo].index[0])
            nombres_poblaciones.append(pueblo)
            temas_calientes.append(str(temas_temp))
        except Exception as e:
            print(e)
        
        

    pueblos_geo = filtrado[filtrado.poblacion.isin(nombres_poblaciones)]#con esto filtramos los pueblos que no tienen temas calientes,
    #hay que sustituir la lista por la lista que devuelva el metodo del wrapper si se llega a hacer, si no pues con todos los pueblos
    centroides = pueblos_geo.centroid #esto saca una lista de los puntos centrales, pero los deja sin nombre ni datos
    #para eso convertimos nuevamente a geodataframe estos puntos y le metemos las columnas necesarias
    gdf_centroides = gpd.GeoDataFrame(centroides, geometry=0)
    print("----nombres poblaciones")
    print(nombres_poblaciones)
    print("----indexes")
    print(indexes)
    print()
    serie_pueblo = pandas.Series(nombres_poblaciones, index=indexes)
    print(serie_pueblo)
    serie_temas = pandas.Series(temas_calientes,index=indexes)
    print(serie_temas)
    gdf_centroides = gdf_centroides.assign(poblacion=serie_pueblo)
    gdf_centroides = gdf_centroides.assign(temas=serie_temas)
    #ahora que ya tenemos los puntos formados con su informacion pertinente lo dibujamos en el mapa
    print(gdf_centroides)