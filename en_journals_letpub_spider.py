import csv
import random
import time
from urllib.parse import urlencode
import requests
import os
from pandas import DataFrame
from lxml.etree import HTML
from bs4 import BeautifulSoup

total_page = 394
letter = 'A'
dirs = './letpub_journals/'


def make_dir(rs):
    if not os.path.exists(rs):
        os.makedirs(rs)


make_dir(rs=dirs)

col = [
    'title',
    'ISSN',
    'star',
    'score',
    'index',
    'quarter',
    'subject',
    'SCI/SCIE',
    'OA',
    'Difficult',
    'period',
    'reader',
    'times',
    'homepage',
    'communicate',
]
journal_frame = DataFrame(columns=col, index=None)
journal_index = 0


def judge(judge_list):
    if len(judge_list) != 0:
        judge_item = ';'.join(judge_list)
        return judge_item.replace('\n', '').replace(';;;', '')
    else:
        judge_item = ''
        return judge_item


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Host': 'www.letpub.com.cn',
    'Referer': 'https://www.letpub.com.cn/index.php?page=journalapp&view=researchfield&fieldtag=&firstletter=A',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}

for page_index in range(0, 10):
    journal_list = []
    payload = {
        'page': 'journalapp',
        'view': 'researchfield',
        'fieldtag': '',
        'firstletter': letter,
        'currentpage': page_index,
    }

    domain = 'http://www.letpub.com.cn/index.php?'
    url = domain + urlencode(payload) + '#journallisttable'
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find_all('table', attrs={'class': 'table_yjfx'})
    soup_son = BeautifulSoup(str(table[0]), 'html.parser')
    tr_list = soup_son.find_all('tr')
    for tr_index in range(2, len(tr_list) - 1):
        soup_child = BeautifulSoup(str(tr_list[tr_index]), 'html.parser')
        item_set = soup_child.find_all('td')
        list_2nd = []
        for item_index in range(len(item_set)):
            dom = HTML(str(item_set[item_index]))
            level_2nd = dom.xpath('//a/text()')
            item_2nd = judge(level_2nd)
            list_2nd.append(item_2nd)
        list_1st = []
        for item_index in range(len(item_set)):
            # print(str(item_set[item_index].string))
            dom = HTML(str(item_set[item_index]))
            level_1st = dom.xpath('*//td/text()')
            item_1st = judge(level_1st)
            list_1st.append(item_1st)
        list_1st.insert(0, list_2nd[1])
        list_3rd = []
        for item_index in range(len(item_set)):
            # print(str(item_set[item_index].string))
            dom = HTML(str(item_set[item_index]))
            level_3rd = dom.xpath('//a/@href')
            item_3rd = judge(level_3rd)
            list_3rd.append(item_3rd)
        list_1st.insert(-1, list_3rd[1])
        list_1st.insert(-2, list_3rd[-2])
        print('--------------', len(list_1st), '----------------')
        journal_list.append(list_1st)
        # journal_frame.loc[journal_index] = list_1st
        # journal_index = journal_index + 1
    tdx = random.randint(1, 10)
    tdy = random.randint(1, 10)
    time.sleep(tdx + tdy / 10)
    with open(dirs + letter + '_' + str(page_index) + '_journal.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for row in journal_list:
            writer.writerow(row)
