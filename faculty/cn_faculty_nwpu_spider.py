import requests
from bs4 import BeautifulSoup
from urllib.parse import urlencode


headers = {
    'Accept': 'text/html, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Length': '81',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'teacher.nwpu.edu.cn',
    'Origin': 'https://teacher.nwpu.edu.cn',
    'Referer': 'https://teacher.nwpu.edu.cn/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    'X-Requested-With': 'XMLHttpRequest',
}

url = 'https://teacher.nwpu.edu.cn/person/searchList.jsp'

form_data = {
    'tit': '01',
    'suf': '',
    'dir': '',
    'sea': '',
    'upd': '',
    'vis': '',
    'xybm': '',
    'zybm': '',
    'xkbm': '',
    'tutor': '',
    'PAGENUMBER': 1,
    'PAGEGROUP': 0,
}

response = requests.post(url=url, data=urlencode(form_data), headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
div_list = soup.find_all('div', attrs={'class': 'col-xs-7'})
