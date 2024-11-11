import json
import requests
import os
from urllib import request, error
from bs4 import BeautifulSoup
from lxml.etree import HTML

img_path = 'ustc/img/'
json_path = 'ustc/json/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(json_path)
make_dir(img_path)

url = 'https://dsxt.ustc.edu.cn/admin_sgdsmd_xnw.asp'
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'http://hr.ustc.edu.cn/',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.50',
}
response = requests.get(url=url, headers=headers)
# print(response.status_code)
soup = BeautifulSoup(response.text, 'html.parser')
tds = soup.find_all('td', attrs={'class': 'q121'})
for td_index in range(len(tds)):
    dom = HTML(str(tds[td_index]))
    urls = dom.xpath('.//a/@href')
    if len(url) != 0:
        for url_index in range(len(urls)):
            personal_url = str(urls[url_index])
            personal_response = requests.get(url=personal_url, headers=headers)
            personal_soup = BeautifulSoup(personal_response.text, 'html.parser')
            name = personal_soup.find_all('td', attrs={'class': 'ustc03'})[0].text
            print(name)
            information = personal_soup.find_all('td', attrs={'class': 'ustc04'})[0].text.replace('  ', '')
            # img_url = personal_soup.find_all('img', attrs={'id': 'zjPhoto'})
            # try:

            #     img = request.urlretrieve('https://dsxt.ustc.edu.cn/' + img_url, img_path + name + '.jpg')
            # except error.HTTPError as e:
            #     pass
            info_dict = {
                'url': personal_url,
                'name': name,
                'information': information,
            }
            faculty_info_json = json.dumps(info_dict, ensure_ascii=False, indent=4)
            with open(json_path + str(name) + '.json', 'w', encoding='utf-8') as f:
                f.write(faculty_info_json)