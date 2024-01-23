import requests
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from lxml import etree
from io import BytesIO
from time import monotonic, sleep
start = monotonic()
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



def NewModle(begin_date, end_date):
    
  da = load_data(begin_date, end_date)
  da = da[da.confirm == '0']
  lst_hsn = [x.lstrip() for x in da['hsn']]
  lst_tsn = [x.lstrip() for x in da['tsn']]
  new_data = pd.DataFrame({'NewModel':[], 'Date':[]})
  new_model = []
  date = []

  driver = webdriver.Chrome()

  url = 'https://www.kfzteile24.de/magazin/ratgeber/hsn-tsn-finden'
  driver.get(url)

  for i, j in zip(lst_hsn, lst_tsn):
      lst = []
      driver.find_element(By.ID, 'input_kba2_new').clear()
      driver.find_element(By.ID, 'input_kba3_new').clear()
      driver.find_element(By.ID, 'input_kba2_new').send_keys(i)
      driver.find_element(By.ID, 'input_kba3_new').send_keys(j)
      time.sleep( 1 )
      elements = driver.find_elements(By.TAG_NAME, 'label')
      for el in elements:(lst).append(el.text)
      str_lst = [x for x in lst if (x != '')&(x != 'zu 2.1/zu 2')&(x != 'zu 2.2/zu 3')]
      t = 'non' if len(str_lst) == 0 else str_lst[0]
      d = 'non' if len(str_lst) == 0 else str_lst[2]
      t, d = ('non', 'non') if len(str_lst) == 0 else (str_lst[0], str_lst[2])
      new_model.append(t)
      date.append(d)
      
      driver.find_element(By.CLASS_NAME, 'close').click()
      time.sleep( 0.8 )
  driver.quit()
  new_data['NewModel'] = new_model
  new_data['Date'] = date
  return pd.concat([da.reset_index(drop=True), new_data.reset_index(drop=True)], axis=1)

da = NewModle('2024-01-01', '2024-01-17')


da.to_csv('new_data.csv')
#3333 bad



end = monotonic()

print(end - start)#43.78200000000652






