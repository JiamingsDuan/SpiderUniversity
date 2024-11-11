import requests
import json
from bs4 import BeautifulSoup
from lxml import etree
from pandas import DataFrame

url = 'https://www.scimagojr.com/journalrank.php'

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                  '96.0.4664.55 Safari/537.36 Edg/96.0.1054.34',
    'X-Requested-With': 'XMLHttpRequest',
}

html = requests.get(url=url, headers=headers)
# print(html.text)
soup = BeautifulSoup(html.text, 'html.parser')
dropdown_all_list = soup.find_all('ul', attrs={'class': 'dropdown-options dropdown-element'})
# for dropdown in dropdown_all_list[2]:
# print(dropdown)
DOM = etree.HTML(str(dropdown_all_list[1]))
xpath_item = '*//ul[@class="dropdown-options dropdown-element"]/'
fetch_list = DOM.xpath(xpath_item + 'li/a[@class="dropdown-element"]/text()')
# print(fetch_list)
subject_frame = DataFrame(columns=['subject'], index=None)

for index, fetch_txt in enumerate(fetch_list):
    subject_frame.loc[index] = [fetch_txt]

subject_frame.to_csv('subject_data.csv', index=False, encoding='utf-8')