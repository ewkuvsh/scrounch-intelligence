
import json
import os
import requests
import sys
import pprint
from bs4 import BeautifulSoup
from dotenv import load_dotenv


load_dotenv()




endpoint =  "https://api.bing.microsoft.com/v7.0/search"
subscription_key = os.environ.get("SUBSCRIPTION_KEY")
#get your own azure key freeloader 


def search(query):

    print("searching web for " + query + "\n\n" )

    mkt = 'en-US'
    params = { 'q': query, 'mkt': mkt, 'responseFilter': {"Webpages","News"},  'count': "1" }
    headers = { 'Ocp-Apim-Subscription-Key': subscription_key }



    response = requests.get(endpoint, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
   
    pages = search_results['webPages']
    results = pages['value']
    output = ""

    
    
    
    for result in results:
        content = requests.get(result['url']).content

        #when in python, just throw imports at the problem and learn nothing yourself 
        soup = BeautifulSoup(content, 'html.parser')
        text = soup.find('body').get_text().strip()

        cleantext = ' '.join(text.split('\n'))
        cleantext = ' '.join(text.split())
        return cleantext

