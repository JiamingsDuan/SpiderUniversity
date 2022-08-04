"""中国期刊网爬虫"""
import requests
from bs4 import BeautifulSoup
from lxml.etree import HTML
from tqdm import tqdm
from mongodb_database import MongoDB

db = MongoDB(host='localhost', db='PaperBox')
total_page = 507
base_url = 'https://www.qikanchina.com/periodical/n'

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'cookie': 'UM_distinctid=17e577c30bc4ad-0d95466558f01e-5e181552-1fa400-17e577c30bd693; '
              'CNZZDATA1278146054=1340054217-1642139697-https%253A%252F%252Fwww.baidu.com%252F%7C1642139697; '
              'Hm_lvt_a20fc759ece77cc4c27acaa92910862e=1642145264,1642145292; '
              'Hm_lpvt_a20fc759ece77cc4c27acaa92910862e=1642145356',
    'referer': 'https://www.qikanchina.com/periodical/p2',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.55',
}


def judge(judge_list):
    if len(judge_list) != 0:
        judge_item = ' '.join(judge_list)
        return judge_item.replace('\n', '').replace('  ', '')
    else:
        judge_item = ''
        return judge_item


for page_index in range(total_page):
    url = base_url + str(page_index)
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    div_set = soup.find_all('div', attrs={'class': 'list-item clearfix'})
    for div_index in tqdm(range(len(div_set))):
        dom = HTML(str(div_set[div_index]))
        img_url_set = dom.xpath('//a[@class="list-item-img"]/img/@src')
        img_url = 'https://www.qikanchina.com' + judge(img_url_set)
        title_set = dom.xpath('//div[@class="mid-tit"]/a/text()')
        title = judge(title_set)
        subject_1_set = dom.xpath('//ul[@class="attribute"]/li[@class="jiaocai"]/a[1]/text()')
        subject_1 = judge(subject_1_set)
        subject_2_set = dom.xpath('//ul[@class="attribute"]/li[@class="jiaocai"]/a[2]/text()')
        subject_2 = judge(subject_2_set)
        ISSN_set = dom.xpath('//ul[@class="attribute"]/li[@class="id-icon"]/text()')
        ISSN = judge(ISSN_set)
        label_set = dom.xpath('//ul[@class="attribute"]/li[@class="feilei"]/a/text()')
        labels = judge(label_set).replace(' ', ';')
        abstract_set = dom.xpath('//ul[@class="attribute"]/li[@class="taojuan"]/p/text()')
        abstract = judge(abstract_set)
        address_set = dom.xpath('//ul[@class="det"]/li[@class="diqu-icon"]/text()')
        address = judge(address_set)
        period_set = dom.xpath('//ul[@class="det"]/li[@class="time-icon"]/text()')
        period = judge(period_set)
        branch_set = dom.xpath('//ul[@class="det"]/li[@class="user-icon"]/a/text()')
        branch = judge(branch_set)
        journal_info_dict = {
            'title': title,
            'img': img_url,
            'subject_1': subject_1,
            'subject_2': subject_2,
            'ISSN': ISSN,
            'labels': labels,
            'abstract': abstract,
            'address': address,
            'period': period,
            'branch': branch,
        }
        # 插入操作
        rep = db.insert_one('mdb_sfm_journal_info_Jnet_2021', journal_info_dict)
