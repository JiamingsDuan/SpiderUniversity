import os
import json
import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from lxml.etree import HTML

TOTAL_PAGE = 1
COLLEGE = '艺术学'
save_path = 'json/'
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
make_dir(img_path)

url = 'https://gr.xjtu.edu.cn/discipline-list?'
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Upgrade-Insecure-Requests': 1,
    'Host': 'gr.xjtu.edu.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}
for page_index in range(TOTAL_PAGE):
    payload = {
        'p_p_id': 'cn_edu_xjtu_gr_home_disciplines_web_XjtuGrHomeWebDisciplinesPortlet_INSTANCE_LFlWP3dmQj2Y',
        'p_p_lifecycle': 0,
        'p_p_state': 'maximized',
        'p_p_mode': 'view',
        '_cn_edu_xjtu_gr_home_disciplines_web_XjtuGrHomeWebDisciplinesPortlet_INSTANCE_LFlWP3dmQj2Y_mvcRenderCommandName': '/disciplines/view_disciplines_teacher',
        '_cn_edu_xjtu_gr_home_disciplines_web_XjtuGrHomeWebDisciplinesPortlet_INSTANCE_LFlWP3dmQj2Y_redirect': '/discipline-list',
        '_cn_edu_xjtu_gr_home_disciplines_web_XjtuGrHomeWebDisciplinesPortlet_INSTANCE_LFlWP3dmQj2Y_sessionVarFlag': 'false',
        '_cn_edu_xjtu_gr_home_disciplines_web_XjtuGrHomeWebDisciplinesPortlet_INSTANCE_LFlWP3dmQj2Y_disciplinesName': COLLEGE,
        '_cn_edu_xjtu_gr_home_disciplines_web_XjtuGrHomeWebDisciplinesPortlet_INSTANCE_LFlWP3dmQj2Y_cur': page_index + 1,
    }

    response = requests.get(url=url+urlencode(payload))
    print(page_index, response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')
    attributes = {
        'class': 'show-quick-actions-on-hover table table-autofit table-heading-nowrap table-list'
    }
    table_list = soup.find_all('table', attrs=attributes)
    soup_tr = BeautifulSoup(str(table_list[0]), 'html.parser')
    tr_list = soup_tr.find_all('tr', attrs={'data-qa-id': 'row'})
    for tr_index in range(len(tr_list)):
        faculty_dict = {}
        dom = HTML(str(tr_list[tr_index]))
        faculty_home_page = dom.xpath('*//td[@class="lfr-xjtu.gr.home.disciplines.teacher.name-column"]/a/@href')
        if len(faculty_home_page) != 0:
            faculty_dict['homepage'] = 'https://gr.xjtu.edu.cn' + faculty_home_page[0]
        else:
            faculty_dict['homepage'] = ''
        faculty_name = dom.xpath('*//td[@class="lfr-xjtu.gr.home.disciplines.teacher.name-column"]/a/text()')
        if len(faculty_name) != 0:
            faculty_dict['faculty'] = faculty_name[0]
        else:
            faculty_dict['faculty'] = ''
        xpath_item = '*//td[@class="lfr-xjtu.gr.home.disciplines.teacher.disciplines-column"]/span/text()'
        faculty_disciplines = dom.xpath(xpath_item)
        if len(faculty_disciplines) != 0:
            faculty_dict['disciplines'] = faculty_disciplines[0]
        else:
            faculty_dict['disciplines'] = ''
        faculty_college = dom.xpath('*//td[@class="lfr-xjtu.gr.home.disciplines.teacher.college-column"]/span/text()')
        if len(faculty_college) != 0:
            faculty_dict['college'] = faculty_college[0]
        else:
            faculty_dict['college'] = ''
        faculty_discipline = dom.xpath('*//td[@class="lfr-xjtu.gr.home.disciplines.teacher.disciplines-column"]/span/text()')
        if len(faculty_discipline) != 0:
            faculty_dict['discipline'] = faculty_discipline[0]
        else:
            faculty_dict['discipline'] = ''
        # print(faculty_dict)
        content_json = json.dumps(faculty_dict, indent=4, ensure_ascii=False)
        with open(save_path + faculty_name[0] + '.json', 'w', encoding='utf-8') as f:
            f.write(content_json)
