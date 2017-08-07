from bs4 import BeautifulSoup
import requests
import time
import pymongo
import random

client    = pymongo.MongoClient('localhost', 27017)
ganji     = client['ganji']
url_list  = ganji['url_list']
url_link  = ganji['url_link']
item_info = ganji['item_info']

headers  = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36 OPR/43.0.2442.1144',
    'Connection' : 'keep-alive'
}

proxy_ip = random.choice([
    'http://125.88.74.122:83',
    'http://112.17.14.47:8080',
    'http://111.13.7.42:82',
    ])
proxies = {'http': proxy_ip}

def get_info(url):
    print(url)
    wb_data = requests.get(url, headers=headers, proxies=proxies)
    if wb_data.status_code == 404:
        pass
    else:
        soup = BeautifulSoup(wb_data.text, 'lxml')
        data = {
            'title'       : soup.select('h1.info_titile')[0].get_text(),
            'price_now'   : soup.select('span.price_now > i')[0].get_text(),
            'price_ori'   : soup.select('span.price_now > b')[0].get_text().split('：')[1].split('元')[0] if soup.find_all("b", class_='price_ori') else None,
            'area'        : soup.select('div.palce_li i')[0].get_text().split('-'),
            'want_person' : soup.select('span.want_person')[0].get_text().split('人')[0],
            'url'         : url
        }
        item_info.insert_one(data)
        # print(data)


def get_list_url(url='http://gz.ganji.com/wu/'):
    url_root = 'http://gz.ganji.com'
    list_urls = []
    wwb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wwb_data.text, 'lxml')
    for tag_a in soup.select('dl.fenlei > dt > a') :
        list_urls.append(url_root + tag_a.get('href'))
        # url_list.insert_one({'list_url' : url_root + tag_a.get('href')})
    # return list_urls
    for i in list_urls:
        print(i)


def get_info_from(list_url, page=1):
    url = list_url + 'o{}'.format(str(page))
    wb_data = requests.get(url, headers=headers)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    if soup.find_all("div", class_='noinfo') or soup.find_all("div", class_='leftBox'):
        pass
    else:
        for tag_a in soup.select('td.t > a.t'):
            url_link.insert_one({'url_link' : tag_a.get('href').split('?')[0]})
            get_info(tag_a.get('href').split('?')[0])
        # print(url_links)

# get_info_from('http://gz.ganji.com/jiaju/', 59)
# get_info_from(get_list_url()[0])
# get_list_url()
# print('原价：100元'.split('：')[1].split('元')[0])