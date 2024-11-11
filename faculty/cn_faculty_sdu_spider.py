import json
import time
import os
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from lxml.etree import HTML
from urllib import request
from tqdm import tqdm


city = '济南'
diciplines = '教学科研辅助及附属单位'
discipline = '山东大学第二附属中学'
discipline_id = 1321
total_page = 1
save_path = 'json/'
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)
base_url = 'https://faculty.sdu.edu.cn/xyjslist.jsp?'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=9C130A3A11F4E5191EC6387F13D156E8',
    'Host': 'faculty.sdu.edu.cn',
    'Referer': 'https://faculty.sdu.edu.cn/xylb.jsp?urltype=tree.TreeTempUrl&wbtreeid=1002',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}
for page_index in range(total_page):
    payload = {
        'totalpage': total_page,
        'PAGENUM': page_index + 1,
        'urltype': 'tsites.CollegeTeacherList',
        'wbtreeid': '1002',
        'st': 0,
        'id': str(discipline_id),
        'lang': 'zh_CN',
    }
    url = base_url + urlencode(payload)
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    div_set = soup.find_all('div', attrs={'id': 'teacher_lists'})
    soup_son = BeautifulSoup(str(div_set[0]), 'html.parser')
    li_list = soup_son.find_all('li', attrs={})
    for li_index in tqdm(range(len(li_list))):
        dom = HTML(str(li_list[li_index]))
        faculty_dict = {}
        home_page = dom.xpath('*//a[@target="_black"]/@href')
        if len(home_page) != 0:
            faculty_dict['homepage'] = home_page[0]
        else:
            faculty_dict['homepage'] = ''
        faculty_name = dom.xpath('*//div[@id="teacher_name"]/text()')
        if len(faculty_name) != 0:
            faculty_dict['faculty_name'] = faculty_name[0]
        else:
            faculty_dict['faculty_name'] = ''
        faculty_degree = dom.xpath('*//div[@id="teacher_degree"]/text()')
        if len(faculty_degree) != 0:
            faculty_dict['faculty_degree'] = faculty_degree[0].split('：')[1]
        else:
            faculty_dict['faculty_degree'] = ''
        faculty_professional = dom.xpath('*//div[@id="teacher_title"]/text()')
        if len(faculty_professional) != 0:
            faculty_dict['faculty_professional'] = faculty_professional[0].split('：')[1]
        else:
            faculty_dict['faculty_professional'] = ''
        img_url = dom.xpath('*//div[@id="teacher_pic"]/img/@src')
        if len(img_url) != 0:
            image_url = 'https://faculty.sdu.edu.cn' + img_url[0]
            try:
                img = request.urlretrieve(image_url, img_path + faculty_name[0] + '.jpg')
            except Exception as e:
                pass
        else:
            pass
        faculty_dict['discipline'] = discipline
        faculty_dict['disciplines'] = diciplines
        faculty_dict['city'] = city
        content_json = json.dumps(faculty_dict, indent=4, ensure_ascii=False)
        with open(save_path + faculty_name[0] + '.json', 'w', encoding='utf-8') as f:
            f.write(content_json)
        time.sleep(0.1)
