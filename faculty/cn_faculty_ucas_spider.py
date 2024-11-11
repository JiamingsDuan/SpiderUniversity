import json
import os
import sys
import requests
from bs4 import BeautifulSoup
from lxml.etree import HTML
from pandas import DataFrame
from tqdm import tqdm
from urllib.parse import urlencode

TITLE = '研究生导师'
code = 77
frame_index = 0
save_path = 'json/'
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'www.ucas.ac.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62 ',
}

# faculty_frame = DataFrame(columns=['faculty_name', 'home_page', 'hat'], index=None)
url = 'https://www.ucas.ac.cn/site/' + str(code)

response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
div_list = soup.find_all('div', attrs={'class': 'yp_sty'})
length = 0

for div_index in range(len(div_list)):
    html = str(div_list[div_index])
    soup_son = BeautifulSoup(html, 'html.parser')
    a_list = soup_son.find_all('a', attrs={'target': '_blank'})
    for a_index in range(len(a_list)):
        faculty_list = []
        dom = HTML(str(a_list[a_index]))
        home_page = dom.xpath('*//a/@href')
        faculty_name = dom.xpath('*//p/text()')
        # print(faculty_name[0], home_page[0])
        faculty_list.append(faculty_name[0])
        faculty_list.append(home_page[0])
        faculty_list.append(TITLE)
        # print(faculty_list)
        faculty_dict = {
            'faculty_name': faculty_name[0],
            'home_page': home_page[0],
            'hat': TITLE,
        }
        journal_info_json = json.dumps(faculty_dict, ensure_ascii=False, indent=4)
        with open(save_path + faculty_name[0] + '.json', 'w', encoding='utf-8') as f:
            f.write(journal_info_json)
        print(faculty_name[0])
