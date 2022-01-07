import os, time, datetime, json, tqdm, glob
from typing import Dict, List
from urllib.request import urlretrieve, build_opener, install_opener
import threading


tqprint = tqdm.tqdm.write

def get_urls_list(API_KEY: str, query: str, pg_number:int = 1, img_number_per_page:int = 10):
    assert pg_number>0 and 1<=img_number_per_page<=80

    # Get image urls with pexels API
    o = os.popen(f'curl -H "Authorization: {API_KEY}" "https://api.pexels.com/v1/search?page={pg_number}&per_page={img_number_per_page}&query={query}"').read()
    o = o.split(',')
    urls = [s[19:-1] for s in o if 'original' in s]

    return urls


def download_from_url_list(url_list: List, query: str, path: str, nr_imgs: int=9999):
    assert len(url_list)>0 and os.path.exists(path)

    opener = build_opener()
    opener.addheaders=[('User-Agent','Mozilla/5.0')]
    install_opener(opener)

    url_list = url_list[:nr_imgs]

    bar = tqdm.tqdm(range(len(url_list)))
    for i, img_url in enumerate(url_list):
        bar.update()

        filename=os.path.join(path, f"{query}_{i:0>4}.{img_url.split('.')[-1]}")
        try:
            # Download image
            # threading.Thread(target=urlretrieve,args=[img_url, filename]).start()
            urlretrieve(img_url, filename)
            
        except Exception as e:
            tqprint(str(e))


def retrieve_images(API_KEY: str ,querys_list: List[str], nr_imgs: int = 100):
    for name in querys_list:

        query = name.replace(' ','_').lower()
        path = f"data/{query}/"
         # Create folders
        if not os.path.isdir(path):
            os.makedirs(path)

        # Get images urls
        if not os.path.isfile(path+'urls.json'):
            urls = []
            for i in range(1,5):
                urls.extend(get_urls_list(API_KEY=API_KEY, query=query, pg_number=i, img_number_per_page=80))

            # Save image urls
            with open(path+'urls.json', 'w') as f:
                json.dump(urls, f, indent=2)
        else:
            with open(path+'urls.json', 'r') as f:
                urls = json.load(f)

        tqprint(f'Number of images urls available for "{query}": {len(urls)}')

        # Download from images urls
        download_from_url_list(urls, query, path, nr_imgs=nr_imgs)


# querys_list = ['cats', 'dogs']
# retrieve_images(querys_list)

