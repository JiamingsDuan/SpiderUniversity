import os
import time
import random
import requests
from pandas import DataFrame
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from lxml.etree import HTML


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
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=78BF779A280060F49CE659E4BF637972',
    'Host': 'scholar.lzu.edu.cn',
    'Referer': 'http://scholar.lzu.edu.cn/browse-author',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}
frame_index = 0
faculty_frame = DataFrame(columns=['home_page', 'faculty_img', 'faculty_name'], index=None)
base_url = 'http://scholar.lzu.edu.cn/browse-author?'
for page_index in range(95):
    tdx = random.randint(1, 10)
    tdy = random.randint(1, 10)
    time.sleep(tdx + tdy / 10)
    payload = {
        'nowpage': page_index + 1,
        'starts_with': '',
        'fangX': 'DESC',
        'paiK': 'workC',
        'sub_flag': '',
        'comm': 0,
    }

    url = base_url + urlencode(payload)
    response = requests.get(url=url, headers=headers)
    # print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    div_list = soup.find_all('div', attrs={'class': 'col-2 mb-2'})
    for div_index in range(len(div_list)):
        faculty_dict = {}
        dom = HTML(str(div_list[div_index]))
        home_page = dom.xpath('*//a/@href')
        if len(home_page) != 0:
            faculty_dict['home_page'] = home_page[0]
        else:
            faculty_dict['home_page'] = ''
        faculty_img = dom.xpath('*//div[@class="block"]/a/img/@src')
        if len(faculty_img) != 0:
            faculty_dict['faculty_img'] = faculty_img[0]
        else:
            faculty_dict['faculty_img'] = ''
        faculty_name = dom.xpath('*//div[@class="font-16 font-weight-normal py-2 text-center"]/text()')
        if len(faculty_name) != 0:
            faculty_dict['faculty_name'] = faculty_name[0]
        else:
            faculty_dict['faculty_name'] = ''
        print('兰州大学:', faculty_name, '个人主页:', home_page, '头像:', faculty_img)
        faculty_frame.loc[frame_index] = [str(item) for item in list(faculty_dict.values())]
        frame_index = frame_index + 1
        tdx = random.randint(1, 5)
        tdy = random.randint(1, 10)
        time.sleep(tdx + tdy / 10)

faculty_frame.to_csv(save_path + 'faculty.csv', index=False, encoding='utf-8')
