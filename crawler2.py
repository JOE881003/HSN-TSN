import requests
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from time import monotonic, sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
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


da = load_data('2024-01-01', '2024-01-17')
da = da[da.confirm == '0']
lst_hsn = [x.lstrip() for x in da['hsn']]
lst_tsn = [x.lstrip() for x in da['tsn']]
new_data = pd.DataFrame({'NewModel2':[], 'Date2':[]})
new_model2 = []
date2 = []


option = webdriver.ChromeOptions()
option.add_argument("headless")
driver = webdriver.Chrome(options = option)


url = 'https://www.dieversicherer.de/versicherer/auto/typklassenabfrage'
driver.get(url)


WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'cmpbntnotxt'))).click()



driver.switch_to.frame('dv-tool-iframe')


WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top"]/main/div/div[2]/div/div/div/div[1]/div/div[2]/button[2]'))).click()



for i, j in zip(lst_hsn, lst_tsn):

    driver.find_element(By.XPATH, '//*[@id="top"]/main/div/div[2]/div/div/div/div[1]/div/div[4]/div/div[1]/div/input').clear()
    driver.find_element(By.XPATH, '//*[@id="top"]/main/div/div[2]/div/div/div/div[1]/div/div[4]/div/div[2]/div/input').clear()
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="top"]/main/div/div[2]/div/div/div/div[1]/div/div[4]/div/div[1]/div/input'))).send_keys(i)
    time.sleep(0.5)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="top"]/main/div/div[2]/div/div/div/div[1]/div/div[4]/div/div[2]/div/input'))).send_keys(j)
    
    time.sleep(0.5)
    a = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ttw-entry__brand'))).text
    b = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ttw-entry__model'))).text
    print('{} {} {} {}'.format(a, b, i, j))
    
    t = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ttw-entry__year'))).text
    new_model2.append('{} {}'.format(a, b))
    date2.append(t)
    
new_data['NewModel2'] = new_model2
new_data['Date2'] = date2
df = pd.concat([da.reset_index(drop=True), new_data.reset_index(drop=True)], axis=1)

end = monotonic()

print(end - start)#31.937999999994645


#df.to_csv('new_data2.csv')







