import os
import re
import time
from urllib import request, error
from urllib.parse import urlencode
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options

# parameter define
# T:5,U:1,V:2,W:3,X:1,Y:1,Z:2
total_page = 5
block = 'T'
# save path
img_path = 'img' + block + '/'


# make save path and create
def make_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


# function
make_dir(img_path)
# base url
base_url = 'http://www.eshukan.com/sci/scijlist.aspx?'
#  instantiation edge browser option
edge_options = Options()
# stop edge browser start
edge_options.add_argument('--headless')
# initialize edge browser start driver
driver = webdriver.Edge(options=edge_options)

# page spider
for page_index in range(1, total_page):
    # payload parameter
    payload = {
        'pg': page_index + 1,
        'firstchar': block,
        'num': 312,
    }
    # splicing the url
    url = base_url + urlencode(payload)
    # request the url
    driver.get(url=url)
    js = 'window.scrollTo(0, document.body.scrollHeight);'
    # exculpatory the driver
    driver.execute_script(js)
    # get the source code
    contents = driver.page_source
    # instantiation the soup
    soup = BeautifulSoup(contents, 'html.parser')
    # analysis the string code and fetch the journals <li><\li> set
    ul_set = soup.find_all('li', attrs={'class': 'bu'})
    # li list spider
    for item_index in range(len(ul_set)):
        time.sleep(0.5)
        # fetch the url
        url = 'http://www.eshukan.com' + ul_set[item_index].a['href']
        # request the url
        driver.get(url=url)
        # get the source code
        contents_ = driver.page_source
        # instantiation the soup
        soup_ = BeautifulSoup(contents_, 'html.parser')
        # search the 'ISSN' string in all over the source string code
        pattern = soup_.find(text=re.compile(r'ISSN'))
        # judge the result
        if pattern is not None:
            # handle string data
            pattern = pattern.replace('  ', '').replace('\n', '')
            ISSN_f = pattern.split('-')[0][-4:]
            ISSN_b = pattern.split('-')[1][:4]
            ISSN = ISSN_f + '-' + ISSN_b
            print(page_index + 1, item_index, ISSN)
            # search the img <div></div>
            img_div = soup_.find_all('div', attrs={'class': 'pic'})
            # judge the result
            if len(img_div) != 0:
                # splicing the image url
                img_url = 'http://www.eshukan.com' + img_div[0].img['src']
                try:
                    # save the image
                    img = request.urlretrieve(img_url, img_path + ISSN + '.jpg')
                except error.HTTPError as e:
                    print(e)
                    pass
            else:
                print('img is none')
                pass
        else:
            pass
