import os
import random
import time
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from lxml.etree import HTML
from pandas import DataFrame
from urllib import request, error
from tqdm import tqdm


total_page = 1
department_code = 30
department_name = '外文系'

save_path = 'json/'
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)
frame_index = 0
faculty_frame = DataFrame(columns=['faculty_name', 'home_page', 'faculty_img', 'department_name'], index=None)

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'referer': 'https://thurid.lib.tsinghua.edu.cn/scholar/?departmentsCode=27',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}
base_url = 'https://thurid.lib.tsinghua.edu.cn/scholar/page?'
payload = {
    'departmentsCode': department_code,
}
for page_index in range(total_page):
    form_data = {
        'nameAcronym': '',
        'realName': '',
        'departmentsCode': department_code,
        'page': page_index + 1,
    }
    url = base_url + urlencode(form_data)
    response = requests.get(url=url, headers=headers)
    # print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    div_list = soup.find_all('div', attrs={'class': 'col-xs-2'})
    # print(len(div_list))

    for div_index in tqdm(range(len(div_list))):
        information_list = []
        dom = HTML(str(div_list[div_index]))
        name = dom.xpath('*//a/@title')
        if len(name) != 0:
            information_list.append(str(name[0]))
            # print(name[0])
        else:
            information_list.append('')
        home_page = dom.xpath('*//a/@href')
        if len(home_page) != 0:
            information_list.append('https://thurid.lib.tsinghua.edu.cn' + str(home_page[0]))
            # print(home_page[0])
        else:
            information_list.append('')
        img_url_list = dom.xpath('*//a/img/@src')
        if len(img_url_list) != 0:
            img_url = 'https://thurid.lib.tsinghua.edu.cn' + img_url_list[0]
            information_list.append(img_url)
            try:
                img = request.urlretrieve(img_url, img_path + information_list[0].replace('?', '') + '.jpg')
            except error.HTTPError as e:
                print(e.code)
                pass
        else:
            information_list.append('')
        information_list.append(department_name)
        faculty_frame.loc[frame_index] = [str(item) for item in information_list]
        frame_index = frame_index + 1
        # print(information_list)
    tdx = random.randint(1, 5)
    tdy = random.randint(1, 10)
    time.sleep(tdx + tdy / 10)
faculty_frame.to_csv(save_path + department_name + '_faculty.csv', index=False, encoding='gbk')
