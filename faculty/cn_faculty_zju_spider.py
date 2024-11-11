import requests
from bs4 import BeautifulSoup
from lxml.etree import HTML

ip_list = []
for page in range(1, 11):
    ips_url = 'http://www.taiyanghttp.com/free/page' + str(page) + '/'
    response = requests.get(url=ips_url)
    ip_contents = response.content
    soup = BeautifulSoup(ip_contents, 'html.parser')
    div_set = soup.find_all('div', attrs={'class': 'tr ip_tr'})

    for index in range(len(div_set)):
        tds = div_set[index]
        dom = HTML(str(tds))
        ip = dom.xpath('.//div/div[1]/text()')[0]
        port = dom.xpath('.//div/div[2]/text()')[0]
        item = str(ip) + ':' + str(port)
        ip_list.append(item)
