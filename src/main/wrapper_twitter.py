from pytwitter import Api
import configparser
import time
import operator
from datetime import datetime

class wrapper_twitter:
  
    def __init__(self):
        self.time = datetime.today().strftime('%Y-%m-%d')
        self.time += 'T00:01:00Z'
        config = configparser.RawConfigParser()
        config.read('keys.conf')
        keys = dict(config.items('KEYS'))
        bearer_token_infoge = keys['bearer']
        self.api = Api(bearer_token=bearer_token_infoge)
        
        
# -- Obtener Cuentas Tweeter a partir de Localizacion -- 
    def getCuentas(self,localizacion):
        try:
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
                result_tw_location = self.api.search_tweets(query=palabra,max_results=100)
                location_data_tweet += result_tw_location.data

            result_list = []
            coleccion_tweets = []
            cont = 0
            for tmp in location_data_tweet:
                coleccion_tweets.insert(0,tmp.id)
                cont +=1
                if cont==100:
                    cont=0
                    infor_result = self.api.get_tweets(coleccion_tweets,tweet_fields=['author_id'])
                    result_list.insert(0,infor_result)
                    coleccion_tweets=[]

            coleccion_infor_tweets = []
            for tmp in result_list:
                for tmp2 in tmp.data:
                    coleccion_infor_tweets.insert(0,tmp2.author_id)

            cont=0
            infor_user_result_list = []
            coleccion_tmp = []
            for tmp in coleccion_infor_tweets:
                coleccion_tmp.insert(0,tmp)
                cont +=1
                if cont==100:
                    cont=0
                    infor_user_result = self.api.get_users(ids=coleccion_tmp)
                    infor_user_result_list.insert(0,infor_user_result)
                    coleccion_tmp=[]

            cuentas_localizacion = []
            for tmp_list in infor_user_result_list:
                for tmp in tmp_list.data:
                    if localizacion in tmp.name or localizacion in  tmp.username:
                        cuentas_localizacion.insert(0,tuple((tmp.id,tmp.name,tmp.username)))

            lista_usernames = []
            for tmp in cuentas_localizacion:
                lista_usernames.insert(0,tmp[2])

            return set(lista_usernames)
        except:
            return []
            

# --Obtener TEMA CALIENTE de una localizacion--
    def getTemasCalientes(self,localizacion):
        try:
            result_hottopic = self.api.search_tweets(query=localizacion,max_results=100)
            datos = result_hottopic.data
            total_tweets_hottopic = ''

            for tmp in datos:
                text = ' ' + tmp.text
                total_tweets_hottopic += text

            palabras = total_tweets_hottopic.split(" ")
            ranking_not_order = {}
            for tmp in palabras:
                ranking_not_order[tmp]=ranking_not_order.get(tmp, 0)+1

            ranking_order = sorted(ranking_not_order.items(), key=operator.itemgetter(1))

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

            i=0
            ranking_top =  []
            while(i<10):
                ranking_top.insert(0,ranking_final[i])
                i+=1

            return ranking_top
        except:
            return []


# -- A partir de una Lista de localizaciones, Obtener las que más Tweets tengan o más se hable --
    def getLocalizacionesCalientes(self,lista_localizaciones):
        try:
            dic_localizaciones = {}
            for localizacion in lista_localizaciones:
                palabras_clave = []
                palabras_clave.insert(0,localizacion)
                if ' ' in localizacion:
                    local_tmp = localizacion.split(" ")
                    palabras_clave.insert(0,'#'+local_tmp[0]+local_tmp[1])
                else:
                    palabras_clave.insert(0,'#'+localizacion)

                location_data_tweet = [] 

                for palabra in palabras_clave:
                    result_tw_location = self.api.search_tweets(query=palabra,start_time=self.time, max_results=100)
                    location_data_tweet += result_tw_location.data
                
                tweets_location = 0
                for tmp in location_data_tweet:
                    tweets_location += 1

                dic_localizaciones[localizacion] = tweets_location

            dic_order = sorted(dic_localizaciones.items(), key=operator.itemgetter(1))
            return dic_order[0]
        except:
            return []


# --Obtener Tweets de un usuario a partir de su user --
    def getTweetsUsuario(self,user):
        try:
            user_result = self.api.get_user(username=user) 
            data_user = user_result.data

            timeline = self.api.get_timelines(user_id=data_user.id,start_time=self.time,max_results=100)
            data_timeline = timeline.data
            tweets_user = []
            for tmp in data_timeline:
                texto_tweet = tmp.text
                if not texto_tweet.startswith('RT'):
                    tweets_user.insert(0,tuple((tmp.id,tmp.text)))

            tweets_finales=[]
            for tmp in tweets_user:
                tweets_finales.insert(0,tmp[1])

            return tweets_finales
        except:
            return []


# --Obtener numero Followers de un Usuario --
    def getFollowersUsuario(self,user):
        try:
            infor_user = self.api.get_user(username=user,user_fields=['public_metrics'])
            data_u = infor_user.data
            followers = data_u.public_metrics.followers_count
            return followers
        except:
            return 0


# --Obtener Numero de Likes que le dan a un  user -- 
    def getLikesUsuario(self,user,diaria):    
        try:
            likes=0
            user_result = self.api.get_user(username=user) 
            data_user = user_result.data

            if diaria==True:
                timeline = self.api.get_timelines(user_id=data_user.id, start_time=self.time, max_results=100)
            else:
                timeline = self.api.get_timelines(user_id=data_user.id, max_results=100)

            data_timeline = timeline.data
            tweets_user = []

            for tmp in data_timeline:
                texto_tweet = tmp.text
                if not texto_tweet.startswith('RT'):
                    tweets_user.insert(0,tuple((tmp.id,tmp.text)))

            coleccion_tweet_id = []
            for tmp in tweets_user:
                coleccion_tweet_id.insert(0,tmp[0])

            infor_tweet = self.api.get_tweets(coleccion_tweet_id,tweet_fields=['public_metrics'])
            for tmp in infor_tweet.data:
                likes+= tmp.public_metrics.like_count

            return likes
        except:
            return 0


# -- Obtener Retweets que le dan a un Usuario --
    def getRetweetsUsuario(self,user,diaria):
        try:  
            retweets=0
            user_result = self.api.get_user(username=user) 
            data_user = user_result.data

            if diaria==True:
                timeline = self.api.get_timelines(user_id=data_user.id, start_time=self.time, max_results=10)
            else:
                timeline = self.api.get_timelines(user_id=data_user.id, max_results=10)

            data_timeline = timeline.data
            tweets_user = []

            for tmp in data_timeline:
                texto_tweet = tmp.text
                if not texto_tweet.startswith('RT'):
                    tweets_user.insert(0,tuple((tmp.id,tmp.text)))

            for tmp in tweets_user:
                usuarios_retweet = self.api.get_tweet_retweeted_users(tweet_id=tmp[0])
                retweets+= len(usuarios_retweet.data)

            return retweets
        except:
            return 0


# --Obtener Vistas Minimas Aproximadas de un Usuario --
    def getVistasUsuario(self,user,diaria):
        try:
            vistas=0
            user_result = self.api.get_user(username=user) 
            data_user = user_result.data

            if diaria==True:
                timeline = self.api.get_timelines(user_id=data_user.id, start_time=self.time, max_results=100)
            else:
                timeline = self.api.get_timelines(user_id=data_user.id, max_results=100)

            data_timeline = timeline.data
            tweets_user = []

            for tmp in data_timeline:
                texto_tweet = tmp.text
                if not texto_tweet.startswith('RT'):
                    tweets_user.insert(0,tuple((tmp.id,tmp.text)))

            coleccion_tweet_id = []
            for tmp in tweets_user:
                coleccion_tweet_id.insert(0,tmp[0])

            infor_tweet = self.api.get_tweets(coleccion_tweet_id,tweet_fields=['public_metrics'])
            for tmp in infor_tweet.data:
                vistas+= tmp.public_metrics.like_count

            for tmp in tweets_user:
                usuarios_retweet = self.api.get_tweet_retweeted_users(tweet_id=tmp[0])
                vistas+= len(usuarios_retweet.data)

            coments_result = self.api.get_tweets(coleccion_tweet_id,tweet_fields=['in_reply_to_user_id'])

            for tmp in coments_result.data:
                if tmp.in_reply_to_user_id is not None:
                    vistas+= 1

            return vistas
        except:
            return 0

# --Obtener Cantidad Tweets de un user -- 
    def getCantidadTweetsUsuarios(self,user, diaria):    
        try:
            likes=0
            user_result = self.api.get_user(username=user) 
            data_user = user_result.data

            if diaria==True:
                timeline = self.api.get_timelines(user_id=data_user.id, start_time=self.time, max_results=100)
            else:
                timeline = self.api.get_timelines(user_id=data_user.id, max_results=100)

            data_timeline = timeline.data
            tweets_user = []

            for tmp in data_timeline:
                texto_tweet = tmp.text
                if not texto_tweet.startswith('RT'):
                    tweets_user.insert(0,tuple((tmp.id,tmp.text)))

            return len(tweets_user)
        except:
            return 0


# --Obtener Cantidad Busquedas de una Localizacion -- 
    def getBusquedas(self, localizacion, diaria):    
        try:
            if diaria==True:
                search_result = self.api.search_tweets(query=localizacion,start_time=self.time, max_results=100)
            else:
                search_result = self.api.search_tweets(query=localizacion, max_results=100)
            datos = search_result.data
            busquedas = 0
            for tmp in datos:
                busquedas+=1
            return busquedas
        except:
            return 0