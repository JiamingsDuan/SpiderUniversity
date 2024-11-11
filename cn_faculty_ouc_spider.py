import requests
from bs4 import BeautifulSoup
from lxml.etree import HTML

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Cookie': 'JSESSIONID=4E4BC2F75C8F901047360A6066EBC94B',
    'Host': 'math.ouc.edu.cn',
    'Referer': 'http://math.ouc.edu.cn/sxx/list.htm',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.71 Safari/537.36 Edg/97.0.1072.62',
}


url = 'http://math.ouc.edu.cn/2017/0410/c8923a61235/page.htm'
response = requests.get(url=url, headers=headers)
print(response.status_code)
soup = BeautifulSoup(response.content, 'lxml')
img_set = soup.find('div', attrs={'class': 'photo bg-blue'})
