import requests
from bs4 import BeautifulSoup
import re
from urllib.request import urlretrieve
import os
import sys

def download_images(articles):
    for article in articles:
        sub_article=re.sub('[#%&*|\:"<>?/]', ' ',article.text)
        sub_article=re.sub(r"^\s+|\s+$", "",sub_article)
        print(sub_article)
        if not os.path.isdir(os.path.join('download',sub_article)):
            os.mkdir(os.path.join('download',sub_article))
        res=requests.get(
            'https://www.ptt.cc/'+article['href'],
            cookies={'over18':'1'}
            )
        images=reg_imgur_file.findall(res.text)
        for image in set(images):
            ID=re.search('http[s]?://[i.]*imgur.com/(\w+\.(?:jpg|png|gif))',image).group(1)
            print(ID)
            urlretrieve(image,os.path.join('download',sub_article,ID))

def crawler(pages):
    print(pages)
    if not os.path.isdir('download'):
        os.mkdir('download')
    url='https://www.ptt.cc/bbs/Beauty/index.html'
    for round in range(pages):
        
        res=requests.get(
            url=url,
            cookies={'over18':'1'}
            )

        soup=BeautifulSoup(res.text,'html.parser')

        articles=soup.select('div.title a')

        paging=soup.select('div.btn-group-paging a')

        next_url='https://www.ptt.cc/'+paging[1]['href']

        url=next_url

        download_images(articles)
        
reg_imgur_file=re.compile('http[s]?://[i.]*imgur.com/\w+\.(?:jpg|png|gif)')

crawler(int(sys.argv[1]))
