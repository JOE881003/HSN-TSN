import requests
import json
import pandas as pd
from lxml import etree
from time import monotonic, sleep
start = monotonic()
class crawler:
    def __init__(self, begin_date, end_date):
        self.begin_date = begin_date
        self.end_date = end_date
        self.load_data()
        self.da = self.da[self.da.confirm == '0']
        self.lst_hsn = [x.lstrip() for x in self.da['hsn']]
        self.lst_tsn = [x.lstrip() for x in self.da['tsn']]
        self.new_data = pd.DataFrame({'NewModel':[], 'Date':[]})
        self.new_model = []
        self.date = []
        for i, j in zip(self.lst_hsn, self.lst_tsn):
            driver = requests.get("https://www.kfzteile24.de/index.cgi?kba2_new={}&kba3_new={}&returnTo=rm%3Dcms&addKfzToGarage=0&rm=carSelectionJson".format(i, j))
            xml_bytes = driver.content
            html = etree.HTML(xml_bytes)
            lst = [html.xpath('//label')[x].text for x in range(len(html.xpath('//label'))) if html.xpath('//label')[x].text is not None]
            d = lst[0]
            t = lst[2]
            self.new_model.append(d)
            self.date.append(t)
        
        self.output_data()
        
        
    def load_data(self):
        url = "https://bento3.orange-electronic.com/SelectMysql"
        payload = "SELECT*FROM orange_userdata.hsn_tsn_confirm where time BETWEEN '{} 00:00:00' and '{} 23:59:59';".format(self.begin_date, self.end_date)
        headers = {
          'Content-Type': 'text/plain'
        }
        
        response = requests.request("POST", url, headers = headers, data = payload)
        x = json.loads(response.text)
        self.da = pd.json_normalize(x)
        
    def output_data(self):
        self.new_data['NewModel'] = self.new_model
        self.new_data['Date'] = self.date
        self.df = pd.concat([self.da.reset_index(drop=True), self.new_data.reset_index(drop=True)], axis=1)
        
        
        
        
        
if __name__ == '__main__':
    # 創建 CalendarMultiSelection 的實例
    da = crawler('2024-01-01', '2024-01-17')   
        
data = da.df

end = monotonic()

print(end - start)#16.719000000011874









