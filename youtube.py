from bs4 import BeautifulSoup as bs
import re
import requests
import pandas as pd
import warnings
from tqdm import tqdm

warnings.filterwarnings("ignore")

def get_youtube_data(url):
    r = requests.get(url,verify=False)
    soup = bs(r.text, "html.parser")
    try:
        result = {}
        result["title"] = soup.find("meta", itemprop="name")['content']
        result["views"] = soup.find("meta",itemprop="interactionCount")['content']
        result["description"] = soup.find("meta",itemprop="description")['content']

        result["tags"] = ', '.join([ meta.attrs.get("content") for meta in soup.find_all("meta", {"property": "og:video:tag"}) ])
        channel_tag = soup.find("meta", itemprop="channelId")['content']
        channel_name = soup.find("span", itemprop="author").next.next['content']
        channel_url = f"https://www.youtube.com/{channel_tag}"
       # channel_subscribers = videoSecondaryInfoRenderer['owner']['videoOwnerRenderer']['subscriberCountText']['accessibility']['accessibilityData']['label']
        result['channel_name'] = channel_name
    except Exception as e:
        print(e)
    #result['Subscribers']=channel_subscribers
    return result

df=pd.read_csv('pf.csv')

a=list(df['Url'].values)
q=[]
for i in tqdm(a):
    #print(i)
    f=get_youtube_data(str(i))
    if len(list(f.keys()))!=1 or f!=[]:
        f['URL']=i
        q.append(f)

s=[]
for i in q:
    if len(list(i.keys()))==6:
           s.append(i)

s=pd.DataFrame(s)

s.to_csv('test.csv')
