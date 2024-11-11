"""letpub期刊爬虫 https://www.letpub.com.cn/ 增强版"""
import json
import re
import random
from time import sleep
import requests
from tqdm import tqdm
from lxml.etree import HTML
from bs4 import BeautifulSoup
# from requests_toolbelt import SSLAdapter

# adapter = SSLAdapter('TLSv1')
# s = requests.Session()
# s.mount('https://', adapter)

save_path = './letpub_journals/json1/'

proxy = '103.215.34.6:8080'

proxies = {
    'http': 'http://' + proxy,
}


def judge(judge_list):
    if len(judge_list) != 0:
        judge_item = ' '.join(judge_list)
        return judge_item.replace('\n', '')
    else:
        judge_item = ''
        return judge_item


def fetch_text(element, item):
    journal_information_set = HTML(str(element)).xpath(item)
    journal_information = judge(journal_information_set)
    return journal_information


# 【1】请求
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': '_ga=GA1.3.909610943.1639118789; PHPSESSID=6kpbh7u960d3gsb9oe83ktq1a1; '
              'Hm_lvt_a94e857ae4207c3ac8fcfd63f6604f22=1642734878,1643001195,1644285124,1644981102; '
              '__utma=189275190.909610943.1639118789.1644297466.1644981102.40; __utmc=189275190; '
              '__utmz=189275190.1644981102.40.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; '
              '_gid=GA1.3.1162174017.1644981102; _gat=1; __utmb=189275190.12.10.1644981102; '
              'Hm_lpvt_a94e857ae4207c3ac8fcfd63f6604f22=1644981118',
    'Host': 'www.letpub.com.cn',
    'Referer': 'https://www.letpub.com.cn/index.php?page=journalapp',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}
for ids in range(1207, 1301):
    url = 'https://www.letpub.com.cn/index.php?page=journalapp&view=detail&journalid=' + str(ids)
    response = requests.get(url=url, headers=headers, proxies=proxies)
    soup = BeautifulSoup(response.text, 'html.parser')
    table_set = soup.find_all('table', attrs={'class': 'table_yjfx'})
    if len(table_set) == 0:
        print(ids, 'wait')
    tr_soup = BeautifulSoup(str(table_set[1]), 'html.parser')

    # 【2】解析
    # title
    pattern_1 = tr_soup.find(text=re.compile(r'期刊名字')).__dict__
    journal_title = fetch_text(pattern_1['next_element'], '*//a/text()')
    print(ids, journal_title)
    # ISSN
    pattern_2 = tr_soup.find(text=re.compile(r'期刊ISSN')).__dict__
    journal_ISSN = fetch_text(pattern_2['next_element'], '*//text()')

    # influence_index
    pattern_3 = tr_soup.find(text=re.compile(r'2020-2021最新IF')).parent.next_sibling.__dict__
    journal_IF = fetch_text(pattern_3['next_element'], '*//text()').replace(' ', '')

    # self_citation
    pattern_4 = tr_soup.find(text=re.compile(r'2020-2021自引率')).__dict__
    journal_SC = fetch_text(pattern_4['next_element'], '*//text()').replace('点击查看自引率趋势图', '').split('%')[0] + '%'

    # H_index
    pattern_5 = tr_soup.find(text=re.compile(r'h-index')).parent.next_sibling.__dict__
    journal_HI = fetch_text(pattern_5['next_element'], '*//text()')

    # cite_score & SJR & ........
    pattern_6 = tr_soup.find(text=re.compile(r'CiteScore')).next_sibling.__dict__
    if fetch_text(pattern_6['next_element'], '*//text()') != '暂无CiteScore数据':
        cite_score_soup = BeautifulSoup(str(pattern_6['next_element']), 'html.parser')
        pattern_6_son = cite_score_soup.find(text=re.compile(r'CiteScore'))
        pattern_6_son = pattern_6_son.parent.parent.next_sibling.__dict__
        journal_cite_score = fetch_text(pattern_6_son['contents'][0], '*//text()')
        journal_SJR = fetch_text(pattern_6_son['contents'][1], '*//text()')
        journal_SNIP = fetch_text(pattern_6_son['contents'][2], '*//text()')
        cite_score_list_soup = BeautifulSoup(str(pattern_6_son['contents'][-1]), 'html.parser')
        pattern_6_grandson = cite_score_list_soup.find_all('tr', attrs={'': ''})

        cite_score_lists = []
        for cite_score_row_index in range(1, len(pattern_6_grandson)):
            cite_score_dict = {'journal_subject': fetch_text(pattern_6_grandson[cite_score_row_index], '*//td[1]/text()'),
                               'journal_quarter': fetch_text(pattern_6_grandson[cite_score_row_index], '*//td[2]/text()'),
                               'journal_queue': fetch_text(pattern_6_grandson[cite_score_row_index], '*//td[3]/text()'),
                               'journal_rate': fetch_text(pattern_6_grandson[cite_score_row_index],
                                                          '*//td[4]/div/div/@lay-percent')}
            cite_score_lists.append(cite_score_dict)
    else:
        journal_cite_score = ''
        journal_SJR = ''
        journal_SNIP = ''
        cite_score_lists = []

    # abstract
    pattern_7 = tr_soup.find(text=re.compile(r'期刊简介')).parent.next_sibling.__dict__
    if len(pattern_7['contents']) != 0:
        journal_abstract = fetch_text(pattern_7['next_element'], '*//text()')
    else:
        journal_abstract = ''

    # authority_url
    pattern_8 = tr_soup.find(text=re.compile(r'期刊官方网站')).parent.next_sibling.__dict__
    journal_authority_url = fetch_text(pattern_8['next_element'], '*//a/@href')

    # send_url
    pattern_9 = tr_soup.find(text=re.compile(r'期刊投稿网址')).parent.next_sibling.__dict__
    journal_send_url = fetch_text(pattern_9['next_element'], '*//a/@href')

    # author_direction_url
    # pattern_10 = tr_soup.find(text=re.compile(r'作者指南网址')).parent.next_sibling.__dict__
    # if len(pattern_10['contents']) != 0:
    #     journal_author_direction_url = fetch_text(pattern_10['next_element'], '*//a/@href')
    # else:
    #     journal_author_direction_url = ''

    # database_open
    pattern_11 = tr_soup.find(text=re.compile(r'是否OA开放访问')).parent.next_sibling.__dict__
    if len(pattern_11['contents']) != 0:
        journal_database_open = fetch_text(pattern_11['next_element'], '*//text()')
    else:
        journal_database_open = ''

    # communication_form
    pattern_12 = tr_soup.find(text=re.compile(r'通讯方式')).parent.next_sibling.__dict__
    if len(pattern_12['contents']) != 0:
        journal_communication_form = fetch_text(pattern_12['next_element'], '*//text()')
    else:
        journal_communication_form = ''

    # publisher
    pattern_13 = tr_soup.find(text=re.compile(r'通讯方式')).parent.next_sibling.__dict__
    if len(pattern_13['contents']) != 0:
        journal_publisher = fetch_text(pattern_13['next_element'], '*//text()')
    else:
        journal_publisher = ''

    # Research directions involved
    pattern_14 = tr_soup.find(text=re.compile(r'涉及的研究方向')).parent.next_sibling.__dict__
    if len(pattern_14['contents']) != 0:
        journal_involved_research_direction = fetch_text(pattern_14['next_element'], '*//text()')
    else:
        journal_involved_research_direction = ''

    # published region or country
    pattern_15 = tr_soup.find(text=re.compile(r'出版国家或地区')).parent.next_sibling.__dict__
    if len(pattern_15['contents']) != 0:
        journal_published_region = fetch_text(pattern_15['next_element'], '*//text()')
    else:
        journal_published_region = ''

    # published language
    pattern_16 = tr_soup.find(text=re.compile(r'出版语言')).parent.next_sibling.__dict__
    if len(pattern_16['contents']) != 0:
        journal_language = fetch_text(pattern_16['next_element'], '*//text()')
    else:
        journal_language = ''

    # published period
    pattern_17 = tr_soup.find(text=re.compile(r'出版周期')).parent.next_sibling.__dict__
    if len(pattern_17['contents']) != 0:
        journal_period = fetch_text(pattern_17['next_element'], '*//text()')
    else:
        journal_period = ''

    # created year
    pattern_18 = tr_soup.find(text=re.compile(r'出版年份')).parent.next_sibling.__dict__
    if len(pattern_18['contents']) != 0:
        journal_created_year = fetch_text(pattern_18['next_element'], '*//text()')
    else:
        journal_created_year = ''

    # articles per year
    pattern_27 = tr_soup.find(text=re.compile(r'年文章数')).parent.next_sibling.__dict__
    if len(pattern_27['contents']) != 0:
        journal_articles = fetch_text(pattern_18['next_element'], '*//text()')
    else:
        journal_articles = ''

    # gold OA rate
    pattern_19 = tr_soup.find(text=re.compile(r'Gold OA文章占比')).parent.next_sibling.__dict__
    if len(pattern_19['contents']) != 0:
        journal_OA_rate = fetch_text(pattern_19['next_element'], '*//text()').split('%')[0] + '%'
    else:
        journal_OA_rate = ''

    # research articles rates
    pattern_20 = tr_soup.find(text=re.compile(r'研究类文章占比')).parent.next_sibling.__dict__
    if len(pattern_27['contents']) != 0:
        journal_research_articles = fetch_text(pattern_20['next_element'], '*//text()')
    else:
        journal_research_articles = ''

    # SCI quarter
    pattern_21 = tr_soup.find(text=re.compile(r'期刊SCI分区')).parent.next_sibling.__dict__
    journal_sci_quarter_soup = BeautifulSoup(str(pattern_21['next_element']), 'html.parser')
    journal_sci_quarter_set = journal_sci_quarter_soup.find_all('tr', attrs={'': ''})

    journal_sci_quarter_list = []
    for journal_sci_quarter_index in range(1, len(journal_sci_quarter_set)):
        journal_sci_quarter_dict = {
            'journal_sci_subject': fetch_text(journal_sci_quarter_set[journal_sci_quarter_index], '*//td/text()'),
            'journal_sci_quarter': fetch_text(journal_sci_quarter_set[journal_sci_quarter_index], '*//td/span['
                                                                                                  '@style="background: '
                                                                                                  '#FFEEEE; border: 1px '
                                                                                                  'solid #FFAAAA; '
                                                                                                  'color:#3b5998; '
                                                                                                  'float:right; '
                                                                                                  'padding:4px;"]/text()'),
        }
        journal_sci_quarter_list.append(journal_sci_quarter_dict)

    # Coverage of SCI Journals
    pattern_22 = tr_soup.find(text=re.compile(r'SCI期刊收录coverage')).parent.next_sibling.__dict__
    journal_sci_coverage_soup = BeautifulSoup(str(pattern_22['parent']), 'html.parser')
    journal_sci_coverage_set = journal_sci_coverage_soup.find_all('a', attrs={'target': '_blank'})
    journal_sci_coverage_list = []
    for journal_sci_coverage_index in range(len(journal_sci_coverage_set)):
        journal_sci_coverage = fetch_text(journal_sci_coverage_set[journal_sci_coverage_index], '*//text()')
        journal_sci_coverage_list.append(journal_sci_coverage)

    # Chinese Academy of Sciences Early warning list
    pattern_23 = tr_soup.find(text=re.compile(r'国际期刊预警')).parent.next_sibling.__dict__
    journal_cas_warning_soup = BeautifulSoup(str(pattern_23['parent']), 'html.parser')
    journal_cas_warning = fetch_text(pattern_23['next_element'], '*//text()')
    # journal_cas_warning_previous = fetch_text(pattern_23['next_element'], '*//br/text()')

    # Average employment ratio
    # pattern_24 = tr_soup.find(text=re.compile(r'平均录用比例')).parent.next_sibling.__dict__
    # journal_average_employment_ratio = fetch_text(pattern_24['next_element'], '*//text()')

    # Division of SCI journals of Chinese Academy of Sciences (latest basic edition in December 2021)
    pattern_25 = tr_soup.find(text=re.compile(r'2021年12月最新基础版')).parent.parent.next_sibling.__dict__
    cas_2021_basic_subject_large = fetch_text(pattern_25['contents'][2], '//table[@width="100%"]/tr[2]/td[1]/text()')
    cas_2021_basic_subject_quarter = fetch_text(pattern_25['contents'][2], '//table[@width="100%"]/tr[2]/td['
                                                                           '1]/span[ '
                                                                           '@style="background: #FFEEEE; '
                                                                           'border: 1px solid #FFAAAA; '
                                                                           'color:#3b5998; '
                                                                           'float:right; padding:4px;"]/text()')

    cas_2021_basic_subject_short_soup = BeautifulSoup(str(pattern_25['contents'][2]), 'html.parser')
    cas_2021_basic_subject_short_table = cas_2021_basic_subject_short_soup.find_all('table', attrs={'width': '99%'})
    if len(cas_2021_basic_subject_short_table) != 0:
        cas_2021_basic_subject_short_soup_son = BeautifulSoup(str(cas_2021_basic_subject_short_table[0]), 'html.parser')
        cas_2021_basic_subject_short_set = cas_2021_basic_subject_short_soup_son.find_all('tr')
        cas_2021_basic_subject_short_list = []
        for cas_2021_basic_subject_short_index in range(len(cas_2021_basic_subject_short_set)):
            subject_short_item = '//tr/td[1]/text()'
            subject_short_quarter_item = '//tr/td[2]/span[@style="background: #FFEEEE; border: 1px solid #FFAAAA; ' \
                                         'color:#3b5998; float:right; padding:4px;"]/text() '
            cas_2021_basic_subject_short_dict = {
                'subject_short': fetch_text(str(cas_2021_basic_subject_short_set[cas_2021_basic_subject_short_index]),
                                            subject_short_item),
                'subject_short_quarter': fetch_text(
                    str(cas_2021_basic_subject_short_set[cas_2021_basic_subject_short_index]),
                    subject_short_quarter_item)
            }
            cas_2021_basic_subject_short_list.append(cas_2021_basic_subject_short_dict)
    else:
        cas_2021_basic_subject_short_list = []
    cas_2021_basic_subject_top = fetch_text(pattern_25['contents'][2], '//table[@width="100%"]/tr[2]/td[3]/text()')
    cas_2021_basic_subject_survey = fetch_text(pattern_25['contents'][2], '//table[@width="100%"]/tr[2]/td[4]/text()')

    # Division of SCI journals of Chinese Academy of Sciences (latest upgrade edition in December 2021)
    pattern_26 = tr_soup.find(text=re.compile(r'2021年12月最新升级版')).parent.parent.next_sibling.__dict__
    cas_2021_upgrade_subject_large = fetch_text(pattern_26['contents'][0], '//table[@width="100%"]/tr[2]/td[1]/text()')
    cas_2021_upgrade_subject_quarter = fetch_text(pattern_26['contents'][0], '//table[@width="100%"]/tr[2]/td['
                                                                             '1]/span[ '
                                                                             '@style="background: #FFEEEE; '
                                                                             'border: 1px solid #FFAAAA; '
                                                                             'color:#3b5998; '
                                                                             'float:right; padding:4px;"]/text()')

    cas_2021_upgrade_subject_short_soup = BeautifulSoup(str(pattern_26['contents'][0]), 'html.parser')
    cas_2021_upgrade_subject_short_table = cas_2021_upgrade_subject_short_soup.find_all('table', attrs={'width': '99%'})
    if len(cas_2021_upgrade_subject_short_table) != 0:
        cas_2021_upgrade_subject_short_soup_son = BeautifulSoup(str(cas_2021_upgrade_subject_short_table[0]), 'html.parser')
        cas_2021_upgrade_subject_short_set = cas_2021_upgrade_subject_short_soup_son.find_all('tr')
        cas_2021_upgrade_subject_short_list = []
        for cas_2021_upgrade_subject_short_index in range(len(cas_2021_upgrade_subject_short_set)):
            subject_short_item = '//tr/td[1]/text()'
            subject_short_quarter_item = '//tr/td[2]/span[@style="background: #FFEEEE; border: 1px solid #FFAAAA; ' \
                                         'color:#3b5998; float:right; padding:4px;"]/text() '
            cas_2021_upgrade_subject_short_dict = {
                'subject_short': fetch_text(str(cas_2021_upgrade_subject_short_set[cas_2021_upgrade_subject_short_index]),
                                            subject_short_item),
                'subject_short_quarter': fetch_text(
                    str(cas_2021_upgrade_subject_short_set[cas_2021_upgrade_subject_short_index]),
                    subject_short_quarter_item)
            }
            cas_2021_upgrade_subject_short_list.append(cas_2021_upgrade_subject_short_dict)
    else:
        cas_2021_upgrade_subject_short_list = []
    cas_2021_upgrade_subject_top = fetch_text(pattern_26['contents'][0], '//table[@width="100%"]/tr[2]/td[3]/text()')
    cas_2021_upgrade_subject_survey = fetch_text(pattern_26['contents'][0], '//table[@width="100%"]/tr[2]/td[4]/text()')

    # against the crawler
    bit = random.randint(7, 10)
    digit = random.randint(7, 10)
    waiting = bit * 10 + digit
    for sec in tqdm(range(waiting)):
        sleep(0.1)

    let_pub = {
        'title': journal_title,
        'ISSN': journal_ISSN,
        'IF': journal_IF,
        'self_citation': journal_SC,
        'H_index': journal_HI,
        'CiteScore': journal_cite_score,
        'SJR': journal_SJR,
        'SNIP': journal_SNIP,
        'CiteScoreRanking': cite_score_lists,
        'introduction': journal_abstract,
        'authority_url': journal_authority_url,
        'contribute_url': journal_send_url,
        'OA': journal_database_open,
        'communication_form': journal_communication_form,
        'publisher': journal_publisher,
        'research_direction': journal_involved_research_direction,
        'region': journal_published_region,
        'language': journal_language,
        'period': journal_period,
        'created_year': journal_created_year,
        'articles': journal_articles,
        'OA_rate': journal_OA_rate,
        'type_research': journal_research_articles,
        'sci_coverage': journal_sci_coverage_list,
        'sci_quarter': journal_sci_quarter_list,
        'cas_basic_large': cas_2021_basic_subject_large,
        'cas_basic_quarter': cas_2021_basic_subject_quarter,
        'cas_basic_short': cas_2021_basic_subject_short_list,
        'cas_basic_top': cas_2021_basic_subject_top,
        'cas_basic_survey': cas_2021_basic_subject_survey,
        'cas_upgrade_large': cas_2021_upgrade_subject_large,
        'cas_upgrade_quarter': cas_2021_upgrade_subject_quarter,
        'cas_upgrade_short': cas_2021_upgrade_subject_short_list,
        'cas_upgrade_top': cas_2021_upgrade_subject_top,
        'cas_upgrade_survey': cas_2021_upgrade_subject_survey,
    }

    # 【3】存储
    journal_info_json = json.dumps(let_pub, ensure_ascii=False, indent=4)
    with open(save_path + str(ids) + '.json', 'w', encoding='utf-8') as f:
        f.write(journal_info_json)
