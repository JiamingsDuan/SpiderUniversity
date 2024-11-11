import json
import os
import requests
import random
from bs4 import BeautifulSoup
from lxml import etree
from cn_journal_user_agent import ua_list

dir_list = os.listdir('images_latex')

print(dir_list)

# 请求头
headers = {
    'User-Agent': random.choice(ua_list)
}

for di in dir_list:
    path = './symbols/' + di + '/'
    base_url = 'https://www.geeksforgeeks.org/' + di + '/'
    symbols_html = requests.post(base_url, headers=headers)
    symbols_html.encoding = 'utf-8'
    # symbols_DOM = etree.HTML(symbols_html.text)
    # symbols_name = symbols_DOM.xpath('*//div[@class="text"]/center/table/tbody/tr[2]/td[3]/text()')
    # print(symbols_html.text)
    soup = BeautifulSoup(symbols_html.text, 'html.parser')
    html_list = soup.find_all('tr')
    # print(html_list)
    tr_list = []
    for html in html_list:
        html_str = str(html).replace('\n', '').replace('  ', '').replace('\t', '')
        tr_list.append(html_str)

    code_dict = {}
    for tr in tr_list:
        DOM = etree.HTML(tr)
        symbols_name = DOM.xpath('//tr/td[1]/text()')
        if len(symbols_name) is not 0:
            # print(symbols_name[0])
            symbols_svg_url = DOM.xpath('//tr/td[2]/img/@src')[0]
            # print(symbols_svg_url)
            symbols_code = DOM.xpath('//tr/td[3]/text()')[0]
            # print(symbols_code)
            img = requests.get(symbols_svg_url)
            f = open(path + symbols_name[0] + '.jpg', 'ab')
            f.write(img.content)  # 多媒体存储content
            f.close()
            code_dict[symbols_name[0]] = symbols_code
            path = 'images/' + di + '/' + symbols_name[0] + '.jpg'
            print(symbols_code, path)
        else:
            pass
    # print(code_dict)
    # path = 'images/' + di + symbols_name[0] + '.jpg'
    # print(path, symbols_code)
    # code_info_json = json.dumps(code_dict, ensure_ascii=False)
    # with open(path + 'code_dict.json', 'w', encoding='utf-8') as f:
    #     f.write(code_info_json)
