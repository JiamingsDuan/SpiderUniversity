import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from lxml.etree import HTML

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Host': 'faculty-cn.tju.edu.cn',
    'Referer': 'http://faculty-cn.tju.edu.cn/xylb.jsp?urltype=tree.TreeTempUrl&wbtreeid=1021',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
}
Base_url = 'http://faculty-cn.tju.edu.cn/xyjslb.jsp?'
payload = {
    'urltype': 'tsites.CollegeTeacherList',
    'wbtreeid': '1021',
    'st': 0,
    'id': 1002,
    'lang': 'zh_CN',
}
url = Base_url + urlencode(payload)
response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
div_list = soup.find_all('div', attrs={'class': 'b-search'})
soup_son = BeautifulSoup(str(div_list[0]), 'html.parser')
li_list = soup_son.find_all('li', attrs={})
for li_index in range(len(li_list)):
    faculty_dict = {}
    dom = HTML(str(li_list[li_index]))
    home_page = dom.xpath('*//a/@href()')
    if len(home_page) != 0:
        faculty_dict['homepage'] = home_page[0]
        print(home_page[0])
    else:
        faculty_dict['homepage'] = ''
    name = dom.xpath('*//')
