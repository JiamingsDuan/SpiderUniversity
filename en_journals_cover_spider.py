import os
import re
import time
import requests
from urllib import request, error
from urllib.parse import urlencode
from bs4 import BeautifulSoup

total_page = 5
block = 'G'
base_url = 'http://www.eshukan.com/sci/scijlist.aspx?'
img_path = 'img' + block + '/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(img_path)

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Host': 'www.eshukan.com',
    'Pragma': 'no-cache',
    'Referer': 'http://www.eshukan.com/sci/SciCate1.aspx',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56',
}
for page_index in range(total_page):
    payload = {
        'pg': page_index + 1,
        'firstchar': block,
        'num': 312,
    }
    response = requests.get(url=base_url + urlencode(payload))
    contents = response.content
    soup = BeautifulSoup(contents, 'html.parser')
    ul_set = soup.find_all('li', attrs={'class': 'bu'})
    for item in ul_set:
        # print()
        time.sleep(0.5)
        url = 'http://www.eshukan.com' + item.a['href']
        response_ = requests.get(url=url, headers=headers)
        soup_ = BeautifulSoup(response_.content, 'html.parser')
        pattern = soup_.find(text=re.compile(r'ISSN'))
        if pattern is not None:
            pattern = pattern.replace('  ', '').replace('\n', '')
            ISSN_f = pattern.split('-')[0][-4:]
            ISSN_b = pattern.split('-')[1][:4]
            ISSN = ISSN_f + '-' + ISSN_b
            print(item.a.text, ISSN)
            img_div = soup_.find_all('div', attrs={'class': 'pic'})
            if len(img_div) != 0:
                img_url = 'http://www.eshukan.com' + img_div[0].img['src']
                try:
                    img = request.urlretrieve(img_url, img_path + ISSN + '.jpg')
                except error.HTTPError as e:
                    print(e)
                    pass
            else:
                print('img is none')
                pass
        else:
            pass
