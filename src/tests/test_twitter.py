from pytwitter import Api
import configparser
import time
import operator

#Obtenemos las Keys del archivo externo
config = configparser.RawConfigParser()
config.read('keys.conf')
keys = dict(config.items('KEYS'))

#Comenzamos con API de Twitter
bearer_token_infoge = keys['bearer']
api = Api(bearer_token=bearer_token_infoge)

# Parametros Generales
user = 'wikicr'

'''
    #### COSAS GENERALES ####
Para hacer comparaciones entre estadisticas, la podemos hacer entre días debido a la limitacion de busqueda de 100 tweets que optenemos de la api.
De esta forma iremos almacenando estadisticas diarias por cada busqueda de localizacion que hagamos y podremos comprar con las anterieres estadisticas
'''

#########################################################################
# -- Obtener Cuentas Tweeter a partir de Localizacion -- 
print('-------------------------- Ejemplo Busqueda Simple de Palabra --------------------------')
localizacion='Madrid'
#A partir de una localizacion sacamos palabras clave para obtener twets y buscar autors de cuentas de Ciudad real.
palabras_clave = []
palabras_clave.insert(0,localizacion)
palabras_clave.insert(0,localizacion.lower())
if ' ' in localizacion:
    local_tmp = localizacion.split(" ")
    palabras_clave.insert(0,'#'+local_tmp[0]+local_tmp[1])
else:
    palabras_clave.insert(0,'#'+localizacion)


location_data_tweet = [] 

for palabra in palabras_clave:
    result_tw_location = api.search_tweets(query=palabra,max_results=20)
    location_data_tweet += result_tw_location.data

#Por cada tweet, obtenemos autores quecontengan en su nombre la localizacion
cuentas_localizacion = []
for tmp in location_data_tweet:
    infor_result = api.get_tweet(tmp.id,tweet_fields=['author_id'])
    infor_user_result = api.get_user(user_id=infor_result.data.author_id)
    if localizacion in infor_user_result.data.name or localizacion in  infor_user_result.data.username:
        cuentas_localizacion.insert(0,tuple((infor_user_result.data.id,infor_user_result.data.name,infor_user_result.data.username)))

print(cuentas_localizacion)
print('\n')

#########################################################################
# -- Ejemplo search -- 
print('-------------------------- Ejemplo Busqueda Simple de Palabra --------------------------')
result = api.search_tweets(query="ciudad real",max_results=10)
#Aqui tenemos el result, y procedemos a sacar el texto de los tweets que obtenemos
datos = result.data
for tmp in datos:
    print('>>',tmp.text) #Tenemos id y text, sacamos solo el texto
print('\n')

#########################################################################
# -- Ejemplo obtener TEMA CALIENTE de una localizacion--
# Para implementar esto hay que fitrar tanto en tweets que contengan 'Ciudad Real' como en tweets propios de la cuenta de Ciu, y obtener palabra o tema mas habaldo
# Tweets propios --> Con lo de tweets de una cuenta en concreto
# Tweets que contengan ciudad real --> un search simple
localizacion = 'Ciudad Real'
print('-------------------------- Tema caliente de localizacion: ',localizacion,' --------------------------')
result_hottopic = api.search_tweets(query=localizacion,max_results=100)
datos = result_hottopic.data
total_tweets_hottopic = ''

#Obtener Tweets una cadena total
for tmp in datos:
    text = ' ' + tmp.text
    total_tweets_hottopic += text

#Obtener diccionario palabras repetidas
palabras = total_tweets_hottopic.split(" ")
ranking_not_order = {}
for tmp in palabras:
    ranking_not_order[tmp]=ranking_not_order.get(tmp, 0)+1

#Ordenar diccionario
ranking_order = sorted(ranking_not_order.items(), key=operator.itemgetter(1))

#Obtener ranking filtrado
black_list = ['a', 'ante', 'bajo', 'cabe', 'con', 'contra', 'de', 'desde', 'durante', 'en', 'entre', 'hacia', 'hasta', 'mediante', 'para', 'por', 'según', 'sin', 'so', 
                    'sobre', 'tras', 'versus', 'vía', 'cabe', 'so','ahora','antes','despues','ayer','hoy','mañana','temprano','todavia','ya','pronto','tarde','aqui','alli',
                    'ahi','alla','cerca','lejos','dentro','fuera','alrededor','encima','detras','delante','despacio','deprisa','bien','mal','como',
                    'mucho','poco','muy','casi','todo','nada','algo','medio','demasiado','bastante','mas','menos','ademas','incluso','tambien','si','también',
                    'no','tampoco','jamas','nunca','acaso','quiza','quizas', 'el','las','los','la','un','unos','unas','una', 'rt', 'fav','!','|','"','@','·','#','$','~','%',
                    '€','&','¬','/','(',')','=','?','¿','¡','ª','º',':',';','.',',','-','_','^','+','*','ç','{','}',']','[','^']
location_word = localizacion.split(' ')
for tmp in location_word:
    black_list.insert(0,tmp.lower())

ranking_final = []
for tmp in ranking_order:
    clave_lower = tmp[0].lower()
    if (clave_lower not in black_list) and (len(clave_lower)>3):
        ranking_final.insert(0,tmp[0])

#print(ranking_final)
#Impimimos top 10 
i=0
while(i<10):
    print(' Ranking Puesto ',i,' --> ',ranking_final[i])
    i+=1
print('\n')

#########################################################################
# -- Ejemplo obtener Tweets de un usuario a partir de su user --
#Obtenemos ID usuario a partir de ID
print('-------------------------- Tweets de User: ',user,' --------------------------')
user_result = api.get_user(username=user) 
data_user = user_result.data

#Obtenemos TIMELINE de usuario, par aluego solo obtener sus tweets
#   Esto lo conseguimos porque si en la timeline un texto de tweet empeiza con RT @user: es un retweet, por lo que
#   lo demas son tweets de la cuenta
timeline = api.get_timelines(user_id=data_user.id,max_results=100)
data_timeline = timeline.data
tweets_user = []
for tmp in data_timeline:
    texto_tweet = tmp.text
    if not texto_tweet.startswith('RT'):
        #print(">>",texto_tweet)
        #Como no podemos trabajar con tipo 'Tweet', ahcemos una lista de tuplas de ID y texto
        tweets_user.insert(0,tuple((tmp.id,tmp.text)))

for tmp in tweets_user:
    print(tmp)
print('\n')


#########################################################################
# -- Ejemplo obtener Followers de un Usuario --
# USER FIELDS -->  [created_at, description, entities, id, location, name, pinned_tweet_id, profile_image_url, protected ,public_metrics , url, username,verified,withheld]
#
print('--------------------------  Seguidores o Followers de User: ',user,' --------------------------')
infor_user = api.get_user(username=user,user_fields=['public_metrics'])
data_u = infor_user.data
print(data_u.public_metrics)
print("Followers de User: ",user,'-->',data_u.public_metrics.followers_count)
print('\n')


#########################################################################
# -- Ejemplo obtener Numero de Likes que le dan a un  user -- 
print('-------------------------- Likes Recientes que tiene User: ',user,' --------------------------')
likes=0
user_result = api.get_user(username=user) 
data_user = user_result.data

timeline = api.get_timelines(user_id=data_user.id,max_results=100)
data_timeline = timeline.data
tweets_user = []

for tmp in data_timeline:
    texto_tweet = tmp.text
    if not texto_tweet.startswith('RT'):
        tweets_user.insert(0,tuple((tmp.id,tmp.text)))

for tmp in tweets_user:
    infor_tweet = api.get_tweet(tweet_id=tmp[0],tweet_fields=['public_metrics'])
    likes+= infor_tweet.data.public_metrics.like_count

print('Likes sobre User:',user,'-->',likes)
print('\n')


#########################################################################
# -- Ejemplo obtener Retweets que le dan a un Usuario --
# A partir de tweets de un usuario, usamos api.get_tweet_retweeted_users(id_tweet) y sumamos la cantidad total de retweeets
print('-------------------------- Retweets Recientes que tiene User: ',user,' --------------------------')
retweets=0
user_result = api.get_user(username=user) 
data_user = user_result.data

timeline = api.get_timelines(user_id=data_user.id,max_results=100)
data_timeline = timeline.data
tweets_user = []

for tmp in data_timeline:
    texto_tweet = tmp.text
    if not texto_tweet.startswith('RT'):
        tweets_user.insert(0,tuple((tmp.id,tmp.text)))

for tmp in tweets_user:
    usuarios_retweet = api.get_tweet_retweeted_users(tweet_id=tmp[0])
    retweets+= len(usuarios_retweet.data)

print('Retweets sobre User:',user,'-->',retweets)
print('\n')


#########################################################################
# -- Ejemplo obtener Vistas Minimas Aproximadas de un Usuario --
# A partir de tweets de un usuario, usamos api.get_tweet con los fields para sacar el numero de impresiones(likes+rt+comment) de cada tweet y sumarlo.
# TWEET FIELDS --> [attachments,author_id,context_annotations,conversation_id,created_at,entities,geo,id,in_reply_to_user_id,lang
#   ,non_public_metrics,organic_metrics,possibly_sensitive,promoted_metrics,public_metrics,referenced_tweets,reply_settings,source,text,withheld]
print('-------------------------- Vistas Recientes que tiene User: ',user,' --------------------------')
vistas=0
user_result = api.get_user(username=user) 
data_user = user_result.data

timeline = api.get_timelines(user_id=data_user.id,max_results=100)
data_timeline = timeline.data
tweets_user = []

for tmp in data_timeline:
    texto_tweet = tmp.text
    if not texto_tweet.startswith('RT'):
        tweets_user.insert(0,tuple((tmp.id,tmp.text)))

#Añadimos likes
for tmp in tweets_user:
    infor_tweet = api.get_tweet(tweet_id=tmp[0],tweet_fields=['public_metrics'])
    vistas+= infor_tweet.data.public_metrics.like_count

#Añadimos RT
for tmp in tweets_user:
    usuarios_retweet = api.get_tweet_retweeted_users(tweet_id=tmp[0])
    vistas+= len(usuarios_retweet.data)

#Añadimos COmentarios
for tmp in tweets_user:
    coments_result = api.get_tweet(tweet_id=tmp[0],tweet_fields=['in_reply_to_user_id'])
    if coments_result.data.in_reply_to_user_id is not None:
        vistas+= 1


print('Vistas Minimas Aproximadas sobre User:',user,'-->',vistas)
print('\n')


#########################################################################
# -- Ejemplo obtener Cantidad de Tweets de un Usuario --





