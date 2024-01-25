import requests
import json
import pandas as pd
from lxml import etree
from time import monotonic, sleep
import os
#start = monotonic()

class crawler:
    def __init__(self, begin_date, end_date):
        self.begin_date = begin_date
        self.end_date = end_date
        self.load_data()
        #self.da = self.da[self.da.confirm == '0']
        new_data = pd.DataFrame({'NewModel':[], 'Date':[]})
        self.da = pd.concat([self.da, new_data], axis=1)
        for i in range(0, len(self.da)):
            if self.da.iloc[i]['confirm'] == '0':
                driver = requests.get("https://www.kfzteile24.de/index.cgi?kba2_new={}&kba3_new={}&returnTo=rm%3Dcms&addKfzToGarage=0&rm=carSelectionJson".format(self.da.iloc[i]['hsn'].lstrip(), self.da.iloc[i]['tsn'].lstrip()))
                xml_bytes = driver.content
                html = etree.HTML(xml_bytes)
                lst = [html.xpath('//label')[x].text for x in range(len(html.xpath('//label'))) if html.xpath('//label')[x].text is not None]
                self.d = lst[0]
                self.t = lst[2]
                
                self.da['NewModel'][i] = self.d
                self.da['Date'][i] = self.t
        
        self.da
        
        
    def load_data(self):
        url = "https://bento3.orange-electronic.com/SelectMysql"
        payload = "SELECT*FROM orange_userdata.hsn_tsn_confirm where time BETWEEN '{} 00:00:00' and '{} 23:59:59';".format(self.begin_date, self.end_date)
        headers = {
          'Content-Type': 'text/plain'
        }
        
        response = requests.request("POST", url, headers = headers, data = payload)
        x = json.loads(response.text)
        self.da = pd.DataFrame(pd.json_normalize(x))
        
    def output_data(self):
        self.new_data['NewModel'] = self.new_model
        self.new_data['Date'] = self.date
        self.df = pd.concat([self.da.reset_index(drop=True), self.new_data.reset_index(drop=True)], axis=1)
        
        
def download_csv(begin_date, end_date, ALL = False):
    dat = crawler(begin_date=begin_date, end_date=end_date)   
    data = dat.da
    if os.path.isdir('HSN-TSN') == False:
        os.makedirs('HSN-TSN')
    if ALL == True:    
        data.to_csv('HSN-TSN/HSN-TSN {} to {}.csv'.format(begin_date, end_date), index = False)
    elif ALL == False:
        data = data[data.confirm == '0']
        data.to_csv('HSN-TSN/HSN-TSN {} to {}.csv'.format(begin_date, end_date), index = False)
        
        
#end = monotonic()
#print(end - start)#16.719000000011874
