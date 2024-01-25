import grequests
import requests
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
from io import BytesIO
from bs4 import BeautifulSoup
import numpy as np
def load_data(begin_date, end_date):
    url = "https://bento3.orange-electronic.com/SelectMysql"
    payload = "SELECT*FROM orange_userdata.hsn_tsn_confirm where time BETWEEN '{} 00:00:00' and '{} 23:59:59';".format(begin_date, end_date)
    headers = {
      'Content-Type': 'text/plain'
    }
    
    response = requests.request("POST", url, headers = headers, data = payload)
    x = json.loads(response.text)
    da = pd.json_normalize(x)
    return da



da = load_data('2024-01-01', '2024-01-17')
da = da[da.confirm == '0']
lst_hsn = [x.lstrip() for x in da['hsn']]
lst_tsn = [x.lstrip() for x in da['tsn']]
new_data = pd.DataFrame({'NewModel':[], 'Date':[]})
new_model = []
date = []

urls = []
for i, j in zip(lst_hsn, lst_tsn):
    urls.append("https://www.kfzteile24.de/index.cgi?kba2_new={}&kba3_new={}&returnTo=rm%3Dcms&addKfzToGarage=0&rm=carSelectionJson".format(i, j))

reqs = (grequests.get(u) for u in urls)
response = grequests.imap(reqs, grequests.Pool(len(urls)))



for r in response:
    soup = r.content
    html = etree.HTML(soup)
    lst = [html.xpath('//label')[x].text for x in range(len(html.xpath('//label'))) if html.xpath('//label')[x].text is not None]
    d = lst[0]
    t = lst[2]
    new_model.append(d)
    date.append(t)
new_data['NewModel'] = new_model
new_data['Date'] = date


data = pd.concat([da.reset_index(drop=True), new_data.reset_index(drop=True)], axis=1)


    





