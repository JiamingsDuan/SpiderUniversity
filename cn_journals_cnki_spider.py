"""知网爬虫"""
import json
import os
import random
import requests
from time import sleep
from urllib import request, error
from bs4 import BeautifulSoup
from lxml.etree import HTML
from urllib.parse import urlencode
from mongodb_database import MongoDB

code = 'A' + '?'
album = '工程科技I'
total_page = 40
save_path = './cnki/' + album + '/json/'
img_path = './cnki/' + album + '/img/'


def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


make_dir(save_path)
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
        'clickName': album,
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
        dom = HTML(str(url_set[url_index]))
        urls = dom.xpath('//a/@href')
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

for page_index in range(total_page):

    urls_set = get_url(page_index + 1)
    for ur in urls_set:

        bit = random.randint(0, 1)
        digit = random.randint(0, 1)
        waiting = bit + digit / 10
        sleep(waiting)

        req = requests.get(url=ur, headers=header)
        # print(req.status_code)
        soup = BeautifulSoup(req.text, 'html.parser')

        # 【0】part-1
        title_box = soup.find_all('h3', attrs={'class': 'titbox'})
        title_dom = HTML(str(title_box[0]))
        cn_title = judge(title_dom.xpath('*//h3/text()'))
        en_title = judge(title_dom.xpath('*//p/text()'))
        title_dict = {
            '中文刊名': cn_title,
            '英文刊名': en_title,
        }
        print(title_dict['中文刊名'])

        # 【1】picture
        # img_url = soup.find('img', attrs={'class': 'pic-book'})['src']
        # try:
        #     img = request.urlretrieve('http:' + img_url, img_path + title_dict['中文刊名'] + '.jpg')
        # except error.HTTPError as e:
        #     pass

        # 【2】part-2
        honor_box = soup.find_all('p', attrs={'class': 'journalType'})
        honor_box_soup = BeautifulSoup(str(honor_box[0]), 'html.parser')
        honor_set = honor_box_soup.find_all('span')
        honor_list = []
        honor_describe = []
        for span_index in range(len(honor_set)):
            honor_dom = HTML(str(honor_set[span_index]))
            honor_item_describe = judge(honor_dom.xpath('//@title'))
            honor_item_bku_core = judge(honor_dom.xpath('//p/text()'))
            honor_item_short = judge(honor_dom.xpath('//text()'))
            honor_list.append(honor_item_bku_core)
            honor_list.append(honor_item_short)
            honor_describe.append(honor_item_describe)
            honor_list = [item for item in honor_list if item != '']
        honor_dict = {
            '期刊收录': honor_list,
            '收录描述': honor_describe,
        }
        # print(honor_dict)

        # 【3】part-3
        base_info_box = soup.find_all('ul', attrs={'id': 'JournalBaseInfo'})
        base_box_soup = BeautifulSoup(str(base_info_box[0]), 'html.parser')
        base_set = base_box_soup.find_all('p')
        base_dict = {}
        for span_index in range(len(base_set)):
            base_dom = HTML(str(base_set[span_index]))
            base_info = judge(base_dom.xpath('//span/text()'))
            base_label = judge(base_dom.xpath('//label/text()'))
            base_dict[base_label] = base_info
        # print(base_dict)

        # 【4】part-4
        publish_info_box = soup.find_all('ul', attrs={'id': 'publishInfo'})
        publish_box_soup = BeautifulSoup(str(publish_info_box[0]), 'html.parser')
        publish_set = publish_box_soup.find_all('p')
        publish_dict = {}
        for span_index in range(len(publish_set)):
            publish_dom = HTML(str(publish_set[span_index]))
            publish_info = judge(publish_dom.xpath('//span/text()'))
            publish_label = judge(publish_dom.xpath('//label/text()'))
            publish_dict[publish_label] = publish_info
        # print(publish_dict)

        # 【5】part-5
        evaluate_info_box = soup.find_all('ul', attrs={'id': 'evaluateInfo'})
        evaluate_index_dict = {}
        if len(evaluate_info_box) != 0:
            evaluate_box_soup = BeautifulSoup(str(evaluate_info_box[0]), 'html.parser')
            evaluate_index_box = evaluate_box_soup.find_all('li')
            evaluate_index_soup = BeautifulSoup(str(evaluate_index_box[1]), 'html.parser')
            evaluate_index_set = evaluate_index_soup.find_all('p', attrs={'class': 'hostUnit'})

            if len(evaluate_index_set) > 2:
                for span_index in range(0, 2):
                    evaluate_index_dom = HTML(str(evaluate_index_set[span_index]))
                    evaluate_index_info = judge(evaluate_index_dom.xpath('//span/text()'))
                    evaluate_index_label = judge(evaluate_index_dom.xpath('//label/text()'))
                    evaluate_index_dict[evaluate_index_label] = evaluate_index_info
            else:
                pass
        else:
            pass

        collect_info_box = soup.find_all('ul', attrs={'id': 'evaluateInfo'})
        collect_database = []
        collect_honor = []
        if len(collect_info_box) != 0:
            # 【6】part-6
            collect_box_soup = BeautifulSoup(str(collect_info_box[0]), 'html.parser')
            collect_info_set = collect_box_soup.find_all('p', attrs={'class': 'database'})

            if len(collect_info_set) > 2:
                for p_index in range(len(collect_info_set)):
                    collect_dom = HTML(str(collect_info_set[p_index]))
                    collect_info = judge(collect_dom.xpath('//text()'))
                    collect_database.append(collect_info)
            else:
                pass
            collect_database_dict = {
                '该刊被以下数据库收录': collect_database,
            }
            # 【7】part-7
            collect_honor_set = collect_box_soup.find_all('p', attrs={'class': 'hostUnit'})

            if len(collect_honor_set) > 3:
                for pp_index in range(len(collect_honor_set)):
                    collect_honor_dom = HTML(str(collect_honor_set[pp_index]))
                    collect_honor_info = judge(collect_honor_dom.xpath('//@title'))
                    collect_honor.append(collect_honor_info)
                collect_honor = [item for item in collect_honor if item != '']
            else:
                pass
            collect_honor_dict = {
                '期刊荣誉': collect_honor,
            }

        else:
            pass

        journal_info_dict = {
            '中文刊名': cn_title,
            '英文刊名': en_title,
            '期刊收录': honor_list,
            '收录描述': honor_describe,
            '基本信息': base_dict,
            '出版信息': publish_dict,
            '评价信息': evaluate_index_dict,
            '北京大学《中文核心期刊要目总览》来源期刊': collect_database,
            '期刊荣誉': collect_honor,
        }

        # save to local
        db = MongoDB(host='localhost', db='PaperBox')
        # 插入操作
        rep = db.insert_one('mdb_sfm_journal_info_cnki_2022', journal_info_dict)
