import os
from datetime import datetime
import time

import re
import urllib.request
import requests
from bs4 import BeautifulSoup

SITE_URL = 'https://open.africa'
PORTAL_URL = SITE_URL + '/dataset/sensorsafrica-airquality-archive-sabaki-nairobi'

if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@custom
def function(*args, **kwargs):

    res = requests.get(PORTAL_URL)
    soup = BeautifulSoup(res.text, 'lxml')
    soup = soup.find("ul", {"class":"resource-list"})

    # create folder if not available
    if  os.path.exists('data/') == False:
        os.mkdir(path='data/', mode=0o777) 

    # Extract data links and titles
    urls = [link.get('href') for link in soup.findAll('a') if '.csv' in link.get('href')]
    titles = [link.get('title') for link in soup.findAll('a') if link.get('title') != None]
    localFiles = os.listdir('data/')

    # Download all available data
    for position in range(len(urls)):
        print(f'checking availability of {titles[position]} data')
        title = (titles[position].lower()+'.csv').replace(' ','_')
        
        # Download missing files
        if title not in localFiles:
            print(f'\tdownloading {titles[position]} data')
            urllib.request.urlretrieve(urls[position], 'data/' + title)
            time.sleep(5)  