from multiprocessing import Pool
from scrapFunc import get_info_from, get_list_url, url_link, item_info
from list_urls import _list_urls
import os


def start(url_list):
    for page in range(1, 80):
        get_info_from(url_list, page)


if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    pool = Pool()
    pool.map(start, _list_urls.split())
    pool.close()
    pool.join()