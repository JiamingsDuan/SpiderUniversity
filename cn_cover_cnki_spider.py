import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
from pymongo import MongoClient
from gridfs import *

base_dir = 'images_cntk/'
base_url = 'https://t.cnki.net/knavi/journals/searchbaseinfo'
headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/91.0.4472.101 Safari/537.36 '
}
searchStateJson = {"StateID": "", "Platfrom": "", "QueryTime": "", "Account": "knavi", "ClientToken": "",
                   "Language": "", "CNode": {"PCode": "JOURNAL", "SMode": "", "OperateT": ""},
                   "QNode": {"SelectT": "", "Select_Fields": "", "S_DBCodes": "", "QGroup": [
                       {"Key": "Navi", "Logic": 1, "Items": [], "ChildItems": [{"Key": "journals", "Logic": 1,
                                                                                "Items": [
                                                                                    {"Key": "subject", "Title": "",
                                                                                     "Logic": 1, "Name": "CCL",
                                                                                     "Operate": "", "Value": "J?",
                                                                                     "ExtendType": 0, "ExtendValue": "",
                                                                                     "Value2": ""}],
                                                                                "ChildItems": []}]}],
                             "OrderBy": "OTA|DESC", "GroupBy": "", "Additon": ""}}

for index in range(1, 107):
    # ajax请求参数
    payload = {
        'searchStateJson': json.dumps(searchStateJson),
        'displaymode': 1,
        'pageindex': index,
        'pagecount': 21,
        'index': 'subject',
        'searchType': '刊名(曾用刊名)',
        'clickName': '社会科学II',
        'switchdata': 'leftnavi'
    }

    # 获取期刊编码
    response = requests.post(base_url, data=payload, headers=headers)
    ul_html = etree.HTML(response.text)
    # print(html.text)
    urls = ul_html.xpath('*//ul[@class="list_tup"]/li/a/@href')
    journal_encode_list = []
    for ur in urls:
        journal_code = ur.split('&')[1].split('=')[1]
        journal_encode_list.append(journal_code)
    # 前往期刊详情页抓取详细信息
    for co in journal_encode_list:
        url = 'https://navi.cnki.net/knavi/journals/' + co + '/detail'
        html = requests.get(url, headers=headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        title = soup.title.string.replace('/', '_')
        cntk_img_url = soup.find('img', attrs={'class': 'pic-book'})['src']
        img = requests.get('http:' + cntk_img_url)
        f = open(base_dir + title + '.jpg', 'ab')
        f.write(img.content)  # 多媒体存储content
        f.close()
        print(title)
        print('-----------')

