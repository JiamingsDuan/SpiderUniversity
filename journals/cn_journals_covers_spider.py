"""期刊封面"""
import json
import os
import random
import re
import requests
from time import sleep
from urllib import request, error
from bs4 import BeautifulSoup
from lxml.etree import HTML
from urllib.parse import urlencode

# B 51, C 60, D 30, E 66, F 75, G 54, H 106, I 31, J 66
code = 'J' + '?'
total_page = 66
img_path = 'img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(img_path)


def judge(judge_list):
    if len(judge_list) != 0:
        judge_item = ' '.join(judge_list)
        return judge_item.replace('\n', '').replace('  ', '')
    else:
        judge_item = ''
        return judge_item


headers = {
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '1133',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'navi.cnki.net',
    'Origin': 'https://navi.cnki.net',
    'Referer': 'https://navi.cnki.net/knavi/journals/index',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
}

data = {"StateID": "", "Platfrom": "", "QueryTime": "", "Account": "knavi", "ClientToken": "", "Language": "",
        "CNode": {"PCode": "JOURNAL", "SMode": "", "OperateT": ""},
        "QNode": {"SelectT": "", "Select_Fields": "", "S_DBCodes": "", "QGroup": [
            {"Key": "Navi", "Logic": 1, "Items": [], "ChildItems": [{"Key": "journals", "Logic": 1, "Items": [
                {"Key": "subject", "Title": "", "Logic": 1, "Name": "CCL", "Operate": "", "Value": code,
                 "ExtendType": 0, "ExtendValue": "", "Value2": ""}], "ChildItems": []}]}], "OrderBy": "OTA|DESC",
                  "GroupBy": "", "Additon": ""}}


def get_url(index):
    form_data = {
        'searchStateJson': json.dumps(data),
        'displaymode': 1,
        'pageindex': index,
        'pagecount': 21,
        'index': 'subject',
        'searchType': '刊名(曾用刊名)',
        'clickName': '',
        'switchdata': 'leftnavi',
        'random': '0.2262045601146303',
    }
    cover_url = 'https://navi.cnki.net/knavi/journals/searchbaseinfo'
    response = requests.post(url=cover_url, headers=headers, data=urlencode(form_data))
    # print(response.status_code)
    cover_soup = BeautifulSoup(response.text, 'html.parser')
    ul_list = cover_soup.find_all('ul', attrs={'class': 'list_tup'})
    soup_son = BeautifulSoup(str(ul_list[0]), 'html.parser')
    url_set = soup_son.find_all('a', attrs={'target': '_blank'})
    url_list = []
    for url_index in range(len(url_set)):
        do = HTML(str(url_set[url_index]))
        urls = do.xpath('//a/@href')
        home_page = 'https://navi.cnki.net' + urls[0]
        url_list.append(home_page)
    return url_list


header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'navi.cnki.net',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}

for page_index in range(28, total_page):

    urls_set = get_url(page_index + 1)
    for ur in urls_set:

        # bit = random.randint(0, 1)
        # digit = random.randint(0, 1)
        # waiting = bit + digit / 10
        # sleep(waiting)

        req = requests.get(url=ur, headers=header)
        soup = BeautifulSoup(req.text, 'html.parser')
        dom = HTML(str(req.text))
        img_url = soup.find('img', attrs={'class': 'pic-book'})['src']
        info_pattern = soup.find('div', attrs={'class': 'listbox clearfix'})
        info_soup = BeautifulSoup(str(info_pattern), 'html.parser')
        pattern = info_soup.find(text=re.compile(r'ISSN'))
        if pattern is not None:
            print(ur)
            pattern = pattern.parent.__dict__['previous_element']
            doms = HTML(str(pattern))
            issn = doms.xpath('//span/text()')
            if len(issn) != 0:
                print(issn[0])
                try:
                    img = request.urlretrieve('https:' + img_url, img_path + issn[0] + '.jpg')
                except error.HTTPError as e:
                    print(e)
                    pass
            else:
                print('error')
                pass
        else:
            pass
