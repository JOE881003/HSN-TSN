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


    


import re
from datetime import datetime

date_string = "2018.01->"

# 使用正則表達式提取日期部分
match = re.search(r'(\d{4})', date_string)
if match:
    start_date_string, end_date_string = match.group()

    # 轉換日期字符串為日期時間物件
    start_date = datetime.strptime(start_date_string, "%Y.%m").strftime('%Y-%m')
    end_date = datetime.strptime(end_date_string, "%Y.%m").strftime('%Y-%m')

    print("Start Date:", start_date)
    print("End Date:", end_date)
else:
    print("日期字符串格式不符合預期。")




import re

# 原始字符串
input_string = "2018.01->"

# 使用正則表達式匹配年份部分
match = re.search(r'(\d{4})', input_string)

# 如果匹配成功，取得年份
if match:
    year = match.group(1)
    print("年份:", year)
else:
    print("未找到匹配的年份。")








X = [3, 3, 3, 4, 5, 6, 7, 8, 8, 9, 10, 10, 10, 10, 15]
np.mean(X)
np.var(X)


import pandas as pd
df = pd.DataFrame({
    'A': [1, 2, 3],
    'B': ['text1\ntext2', 'text3\nmoretext', 'another\nexample']
})

# 顯示原始 DataFrame
print("原始 DataFrame:")
print(df)

# 要拆分的行索引
row_index_to_split = 0

# 取得要拆分的那一行
row_to_split = df.iloc[row_index_to_split]

# 將該行複製一份並修改需要拆分的值
new_row = row_to_split.copy()
new_row['B'] = row_to_split['B'].split('\n')[1]  # 假設以 \n 分割，這裡取第二部分

# 在原 DataFrame 中插入新行
df = pd.concat(df, pd.DataFrame(new_row), ignore_index=True)

# 顯示更新後的 DataFrame
print("\n更新後的 DataFrame:")
print(df)


a = 'abcdef'
a.split('\n')


