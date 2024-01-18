from bs4 import BeautifulSoup
import pandas as pd
import requests
import numpy as np
from datetime import datetime
#from urllib.request import urlopen


data_film_platform = pd.DataFrame()

for platform in ['netflix', 'disney_plus', 'amazon_prime']:
    print(platform)
    for pagina in range(10):
        
        URL = "https://www.rottentomatoes.com/browse/movies_at_home/affiliates:"+str(platform)+"~sort:popular?page="+str(pagina+1)
        
        page = requests.get(URL)
        
        soup = BeautifulSoup(page.content, "html.parser")
        
        
        results = soup.find(id="main-page-content")
        
        
        #job_elements = results.find_all("score-pairs")
        #titolo       = results.find_all('span', class_ = 'p--small')
        
        lista_film = results.find_all(('a','div'),{'data-track' : 'scores', 'data-qa' : 'discovery-media-list-item-caption'})
        
        lista_film_clean = lista_film[0:len(lista_film)]
        
        
        
        aud_score = []
        aud_sentiment = []
        crit_score = []
        crit_sentiment = []
        titolo = []
        data_rec = []
        
        for i in range(len(lista_film_clean)):
            # estraggo parti in html
            scores_html = lista_film_clean[i].find("score-pairs-deprecated")
            titolo.append(lista_film_clean[i].find('span', class_ = 'p--small').text.strip())
            data_rec.append(lista_film_clean[i].find('span', class_ = 'smaller').text.strip())
            
            # 
            aud_score.append(scores_html.get("audiencescore"))
            aud_sentiment.append(scores_html.get("audiencesentiment"))
            crit_score.append(scores_html.get("criticsscore"))
            crit_sentiment.append(scores_html.get("criticssentiment"))
            
        # riempio bf
        data_film = pd.DataFrame()

        data_film['titolo']   = titolo
        data_film['data_rec'] = data_rec
        data_film['audience_score'] = aud_score
        data_film['critics_score'] = crit_score
        data_film['audience_sentiment'] = aud_sentiment
        data_film['critics_sentiment'] = crit_sentiment
        data_film['piattaforma'] = platform
        
        print('webpage:', pagina)
    
    data_film_platform = pd.concat([data_film_platform, data_film], axis = 0)
    
# estraggo migliori film per ogni platform

data_film_platform['audience_score'] = pd.to_numeric(data_film_platform['audience_score'])
data_film_platform['critics_score'] = pd.to_numeric(data_film_platform['critics_score'])

data_film_platform['audience_score'] = data_film_platform['audience_score'].apply(lambda x: 0 if x == np.nan else x)
data_film_platform['critics_score']  = data_film_platform['critics_score'].apply(lambda x: 0 if x == np.nan else x)

data_film_platform['film_rate'] = (data_film_platform['audience_score']+data_film_platform['critics_score'])/2


data_film_platform['anno_film'] = data_film_platform['data_rec'].apply([lambda anno: int(anno[-4:])])

data_film_platform['data_tot'] = data_film_platform['data_rec'].apply([lambda data_fin: data_fin.replace('Streaming ', '')])

def eta_film(anno):
    if(anno >2010):
    	return "2010-oggi"
    elif(anno >2000 and anno<2010): 
        return "2000-2010"
    elif(anno >1990 and anno<2000):
        return "90-2000"
    elif(anno >1980 and anno<1990):
        return "80-90"
    # an exact match is not confirmed, this last case will be used if provided
    else:
        return "<80"



data_film_platform['periodo'] = data_film_platform['anno_film'].apply(lambda x: eta_film(x))

data_film_platform['data_rec'] = data_film_platform['data_tot']#.apply(lambda x:datetime.strptime(x, "%b %d, %Y").strftime("%d-%m-%Y"))
data_film_platform.drop('data_tot', inplace=True, axis=1)
data_film_platform["data_recensione_film"]=(datetime.now() - pd.to_datetime(data_film_platform['data_rec'])).apply(lambda x:abs(x.days))

top_film_x_plat     = data_film_platform.sort_values(['audience_score', 'critics_score'], ascending=[False, False]).\
    groupby('piattaforma').head(3).reset_index().sort_values('piattaforma').reset_index(drop=True)
top_film_x_plat_tot = data_film_platform.sort_values(['film_rate'], ascending=False).\
    groupby('piattaforma').head(3).reset_index().sort_values('piattaforma').reset_index(drop=True)
top_film_recenti    = data_film_platform[data_film_platform["data_recensione_film"]<30].\
    sort_values(['audience_score', 'critics_score'], ascending=[False, False]).groupby('piattaforma').head(20).reset_index()


script_txt = "-----------------------------------------\n"+\
          "\nfilm recenti : \n"+\
          top_film_recenti[["titolo", "piattaforma","audience_score", "critics_score"]].to_markdown()+\
          "\n\ntop film per audience e critic score: \n "+\
          top_film_x_plat[["titolo", "piattaforma","audience_score", "critics_score"]].to_markdown()+\
          "\n\ntop film per score medio: \n"+\
          top_film_x_plat_tot[["titolo", "piattaforma","audience_score", "critics_score"]].to_markdown()+\
          "\n-----------------------------------------\n"


with open('/home/clair/Documents/formazione/web_scraping/movies_web_scraping/txt_output/best_films.txt', 'w') as f:
    f.write(script_txt)


