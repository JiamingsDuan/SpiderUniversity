import os
import time
import json
import requests
from urllib import request
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from lxml.etree import HTML
from tqdm import tqdm

total_page = 1
college_id = 2007
disciplines = '研究院'
save_path = 'json/'
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)

base_url = 'https://faculty.sjtu.edu.cn/xyjs_list.jsp?'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Host': 'faculty.上交sjtu.edu.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}
for page_index in range(total_page):
    payload = {
        'totalpage': total_page,
        'PAGENUM': page_index,
        'urltype': 'tsites.CollegeTeacherList',
        'wbtreeid': 1011,
        'st': 0,
        'id': college_id,
        'lang': 'zh_CN',
    }
    url = base_url + urlencode(payload)
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    div_list = soup.find_all('div', attrs={'class': 'list'})
    soup_son = BeautifulSoup(str(div_list[0]), 'html.parser')
    li_list = soup_son.find_all('li', attrs={})
    for li_index in tqdm(range(len(li_list))):
        faculty_dict = {}
        dom = HTML(str(li_list[li_index]))
        home_page = dom.xpath('*//a[@target="_blank"]/@href')
        if len(home_page) != 0:
            faculty_dict['homepage'] = home_page[0]
        else:
            faculty_dict['homepage'] = ''
        faculty_name = dom.xpath('*//div[@class="name"]/text()')
        if len(faculty_name) != 0:
            faculty_dict['faculty_name'] = faculty_name[0]
        else:
            faculty_dict['faculty_name'] = ''
        faculty_department = dom.xpath('*//div[@class="js"]/p[1]/text()')
        if len(faculty_department) != 0:
            faculty_dict['faculty_department'] = faculty_department[0].split('：')[1]
        else:
            faculty_dict['faculty_department'] = ''
        faculty_professional = dom.xpath('*//div[@class="js"]/p[2]/text()')
        if len(faculty_professional) != 0:
            faculty_dict['faculty_professional'] = faculty_professional[0].split('：')[1]
        else:
            faculty_dict['faculty_professional'] = ''
        faculty_abstract = dom.xpath('*//div[@class="js"]/p[3]/text()')
        if len(faculty_abstract) != 0:
            faculty_dict['faculty_abstract'] = faculty_abstract[0].replace(' ', '')
        else:
            faculty_dict['faculty_abstract'] = ''
        img_url = dom.xpath('*//div[@class="pic"]/img/@src')
        if len(img_url) != 0:
            image_url = 'https://faculty.sjtu.edu.cn' + img_url[0]
            try:
                img = request.urlretrieve(image_url, img_path + faculty_name[0] + '.jpg')
            except Exception as e:
                pass
        else:
            pass
        faculty_dict['disciplines'] = disciplines
        content_json = json.dumps(faculty_dict, indent=4, ensure_ascii=False)
        with open(save_path + faculty_name[0] + '.json', 'w', encoding='utf-8') as f:
            f.write(content_json)
        time.sleep(0.1)
