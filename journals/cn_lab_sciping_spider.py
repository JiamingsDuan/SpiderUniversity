"""国家重点实验室爬虫"""
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
              'application/signed-exchange;v=b3;q=0.9',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'no-cache',
    'cookie': '_ga=GA1.2.1079438402.1642906470; _gid=GA1.2.1223428250.1642906470; '
              'Hm_lvt_921b893ec658ace0ebbf9ba1a18b0b80=1642906214,1642906571; '
              'Hm_lpvt_921b893ec658ace0ebbf9ba1a18b0b80=1642906574',
    'pragma': 'no-cache',
    'referer': 'https://www.sciping.com/13188.html',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/97.0.4692.99 Safari/537.36 Edg/97.0.1072.69',
}

url = 'https://www.sciping.com/13188.html'
response = requests.get(url=url, headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
frame = DataFrame(columns=['领域', '实验室名称', '依托单位', '主管部门', '主任', '联系人', '电话'])


def fetch(index):
    frame_index = 0
    ids = 'tablepress-' + str(index)
    classes = 'tablepress-table-name tablepress-table-name-id-' + str(index)
    table_set = soup.find_all('table', attrs={'id': ids})
    area = soup.find_all('h2', attrs={'class': classes})
    title = area[0].text.split('-')[1]
    soup_son = BeautifulSoup(str(table_set[0]), 'html.parser')
    tr_set = soup_son.find_all('tr', attrs={'': ''})
    for tr_index in range(len(tr_set)):
        table_soup_2 = BeautifulSoup(str(tr_set[tr_index]), 'html.parser')
        td_set = table_soup_2.find_all('td', attrs={'': ''})
        info = []
        for td_index in range(len(td_set)):
            text = td_set[td_index].text.replace('\n', '').split('[')[0]
            info.append(text)
        if len(info) != 0:
            info.insert(0, title)
            frame.loc[frame_index] = info
            frame_index = frame_index + 1
    return frame


def fetch_1(index):
    frame_index = 0
    ids = 'tablepress-' + str(index)
    classes = 'tablepress-table-name tablepress-table-name-id-' + str(index)
    table_set = soup.find_all('table', attrs={'id': ids})
    area = soup.find_all('h2', attrs={'class': classes})
    title = area[0].text
    soup_son = BeautifulSoup(str(table_set[0]), 'html.parser')
    tr_set = soup_son.find_all('tr', attrs={'': ''})
    for tr_index in range(len(tr_set)):
        table_soup_2 = BeautifulSoup(str(tr_set[tr_index]), 'html.parser')
        td_set = table_soup_2.find_all('td', attrs={'': ''})
        info = []
        for td_index in range(len(td_set)):
            text = td_set[td_index].text.replace(' ', '').replace('\n', '').split('[')[0]
            info.append(text)
        if len(info) != 0:
            info.insert(0, title)
            print(info)
            frame.loc[frame_index] = info
            frame_index = frame_index + 1
    return frame


def to_csv(index):
    frame_index = fetch(index)
    frame_index.to_csv('laboratory/laboratory_utf8_' + str(index) + '.csv', index=True, encoding='GBK')


def to_csv_1(index):
    frame_index = fetch_1(index)
    frame_index.to_csv('laboratory/laboratory_utf8_' + str(index) + '.csv', index=True, encoding='GBK')


if __name__ == '__main__':
    to_csv_1(32)
    for i in range(24, 32):
        to_csv(i)
