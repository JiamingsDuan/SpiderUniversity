import requests
import random
import time
from lxml import etree
from cn_journal_user_agent import ua_list
from bs4 import BeautifulSoup
from mongodb_initialization import MongoDB
from tqdm import tqdm

headers = {
    'X-Requested-With': 'XMLHttpRequest',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'text/html; charset=UTF-8',
    'User-Agent': random.choice(ua_list)
}
db = MongoDB(host='localhost', db='test')

for page_index in range(1, 36):
    time.sleep(random.randint(0, 1))
    targetUrl = 'https://www.medsci.cn/sci/nsfc.do?page=' + str(
        page_index) + '&date_begin=2019&date_end=2020&project_classname_list=面上项目&sort_type=3'
    try:
        html = requests.get(url=targetUrl, headers=headers)
        html.content.decode('utf-8')
        soup = BeautifulSoup(html.text, 'html.parser')
        html_list = soup.find_all('div', attrs={'class': 'journal-item flex'})
        for item in tqdm(html_list):
            # 转码
            DOM = etree.HTML(str(item))
            # 项目地址
            ms_url = DOM.xpath('*//div[@class="journal-item flex"]/div[@class="item-font"]/strong['
                               '@class="m-b-10"]/a/@href')
            Foundation_url = ms_url[0]
            html_son = requests.get(url=Foundation_url, headers=headers)
            DOM_son = etree.HTML(html_son.text)
            # 详细信息
            xpath_item = '*//div[@class="journal-content"]/'
            # 项目名称
            title = DOM_son.xpath(xpath_item + 'div[2]/div[2]/div[1]/span[@class="font-black"]/text()')[0].replace('\t', '')
            Foundation_dict = {'Title': title}
            # 项目编号
            number = DOM_son.xpath(xpath_item + 'div[3]/div[2]/div[1]/span[@class="font-black"]/text()')[0].replace('\t',
                                                                                                                    '')
            # 学科分类代码
            Foundation_dict['number'] = number
            subject_code = DOM_son.xpath(xpath_item + 'div[4]/div[2]/div[1]/span[@class="font-black"]/span[1]/text()')[
                0].replace('\t', '')
            Foundation_dict['subject_code'] = subject_code
            # 学科分类
            subject = DOM_son.xpath(xpath_item + 'div[4]/div[2]/div[1]/span[@class="font-black"]/span[2]/text()')[
                0].replace('\t', '')
            Foundation_dict['subject'] = subject
            # 资助类型
            subsidize = DOM_son.xpath(xpath_item + 'div[5]/div[2]/div[1]/span[@class="font-black"]/text()')[0].replace('\t',
                                                                                                                       '')
            Foundation_dict['subsidize'] = subsidize
            # 负责人
            organizer = DOM_son.xpath(xpath_item + 'div[6]/div[2]/div[1]/span[@class="font-black"]/text()')[0].replace('\t',
                                                                                                                       '')
            Foundation_dict['organizer'] = organizer
            # 依托单位
            organization = DOM_son.xpath(xpath_item + 'div[7]/div[2]/div[1]/span[@class="font-black"]/text()')[0].replace(
                '\t', '')
            Foundation_dict['organization'] = organization
            # 批准年份
            ratify_year = DOM_son.xpath(xpath_item + 'div[8]/div[2]/div[1]/span[@class="font-black"]/text()')[0].replace(
                '\t', '')
            Foundation_dict['ratify_year'] = ratify_year
            # start_time
            start_stop = DOM_son.xpath(xpath_item + 'div[9]/div[2]/div[1]/span[@class="font-black"]/text()')[0].replace(
                '\t', '')
            Foundation_dict['start_stop'] = start_stop
            # 批准金额
            ratify_much = DOM_son.xpath(xpath_item + 'div[10]/div[2]/div[1]/span[@class="font-black"]/text()')[0].replace(
                '\t', '')
            Foundation_dict['ratify_much'] = ratify_much
            # 摘要
            abstract = DOM_son.xpath(xpath_item + 'div[11]/div[2]/div[1]/span[@class="font-black"]/text()')[0].replace('\t',
                                                                                                                       '')
            Foundation_dict['abstract'] = abstract
            # 插入操作
            rep = db.insert_one('mdb_sfm_foundation_mianshang_item', Foundation_dict)
            # print(Foundation_dict)
            # time.sleep(random.randint(0, 1))
    except requests.exceptions.ConnectionError as e:
        print('Error', e)
