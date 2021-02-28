import requests
import json
import time
import pandas as pd
from re import sub
from decimal import Decimal
from bs4 import BeautifulSoup as bs4

class ZillowScraper():
    results = []
    data ={
        'Address': [],
        'Price': [],
        'BedRoom': [],
        'BathRoom': [],
        'SquareFt':[],
        'HouseType': [],
        'YearBuilt': [],
        'Heating': [],
        'Cooling': [],
        'Parking': [],
        'PriceSqft':[]
        }
    headers = {
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': 'JSESSIONID=C4EF40936F90961A7795A88BF1E67551; zguid=23|$c0dce7ad-b1ce-488a-a51a-8af723df938c; zgsession=1|7b932435-0296-46eb-82e0-2862ea20e64a; zjs_user_id=null; zjs_anonymous_id="c0dce7ad-b1ce-488a-a51a-8af723df938c"; _pxvid=c7de5fb7-73b6-11eb-bd3d-0242ac120018; _pxff_cc=U2FtZVNpdGU9TGF4Ow==; _pxff_bsco=1; _px3=fda0abc877c3c39cbba19d9e8ad35bab2ed46435b8c4a16a1d494d6e33734c5d:yWpX6W2w0TZwsFDC4tOK0Lpg3Hvj/ZR2ISGFGoufD1YGWtFO6pv97UA+GMaWrTz60uxjb5yxEgyNQfh++AIHkQ==:1000:V5trV/w/bnIS5k+tZGpmylsM+hDkBewjkDFueK6wovpfJwVpbQfkymFQa+06aFw9783SKflRjXHpXoTm+1KYPnEVFOFkw1OMWfyiS42mnB/AQ9PdDcHMnENilGEzeWZaUJAboy70seBNwKN148kBtXDwDsQ2rQjxsQ55TG3CwUQ=; AWSALB=zZGk+XKJpbDKt0HCVXiFczWGbWpFSQBjYZIgeyFyXz4EAgkej6/vfdBmAP+EqW3WgpW1QaabwcaFh9HUAojCFhqwEu3wEtnRlmcxEh50RLhiQaabUgKlBzdOQ62w; AWSALBCORS=zZGk+XKJpbDKt0HCVXiFczWGbWpFSQBjYZIgeyFyXz4EAgkej6/vfdBmAP+EqW3WgpW1QaabwcaFh9HUAojCFhqwEu3wEtnRlmcxEh50RLhiQaabUgKlBzdOQ62w; search=6|1616443483896|rect=40.116038734291635%2C-75.49456646921072%2C39.896717139073374%2C-75.72871258737479&rid=65895&disp=map&mdm=auto&p=1&z=0&pt=pmf%2Cpf&fs=1&fr=0&mmm=1&rs=0&ah=0&singlestory=0&housing-connector=0&abo=0&garage=0&pool=0&ac=0&waterfront=0&finished=0&unfinished=0&cityview=0&mountainview=0&parkview=0&waterview=0&hoadata=1&zillow-owned=0&3dhome=0'								,
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36'
    }

    def fetch(self, url):
        response = requests.get(url, headers=self.headers)
        print(response.status_code)
        return response

    def parse(self, response):
        content = bs4(response, 'lxml')
        deck = content.find('ul', {'class': 'photo-cards photo-cards_wow photo-cards_short photo-cards_extra-attribution'})
        for card in deck.contents:
            script = card.find('script', {'type': 'application/ld+json'})
            if script:
                script_json = json.loads(script.contents[0])
                self.results.append(script_json['url'])

    def parse2(self,response):
        content = bs4(response, 'lxml')
        Address = content.find('div',{'class':'Text-c11n-8-18-0__aiai24-0 hweBDL ds-price-change-address-row'})
        self.data['Address'].append(Address.text)
        Price = content.find('span',{'class':'Text-c11n-8-18-0__aiai24-0 sc-pYA-dN lcoQFe'})
        self.data['Price'].append(Price.text)

        Top = content.find_all('span',{'class':'ds-bed-bath-living-area'})
        self.data['BedRoom'].append(Top[0].get_text())
        self.data['BathRoom'].append(Top[1].get_text())
        self.data['SquareFt'].append(Top[2].get_text())

        Facts = content.find_all('span',{'class':'Text-c11n-8-18-0__aiai24-0 sc-pczax cYlXJg'})
        self.data['HouseType'].append(Facts[0].get_text())
        self.data['YearBuilt'].append(Facts[1].get_text())
        self.data['Heating'].append(Facts[2].get_text())
        self.data['Cooling'].append(Facts[3].get_text())
        self.data['Parking'].append(Facts[4].get_text())

        price2 = Decimal(sub(r'[^\d]', '', Price.text))
        squareFt = Decimal(sub(r'[^\d]', '', Top[2].get_text()))
        priceSqft = round(price2 / squareFt)
        self.data['PriceSqft'] = priceSqft


    def getPageInfo(self):
        for i in self.results[:1]:
            response = self.fetch(i)
            self.parse2(response.text)
            time.sleep(10)

    def to_csv(self):
        output_df = pd.DataFrame.from_dict(self.data)
        output_df.to_csv("ZillowData.csv",index=False)

    def run(self):
        #url = 'https://www.zillow.com/west-chester-pa-19380/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%2219380%22%2C%22mapBounds%22%3A%7B%22west%22%3A-75.81248333932791%2C%22east%22%3A-75.4107957172576%2C%22south%22%3A39.896717139073374%2C%22north%22%3A40.116038734291635%7D%2C%22mapZoom%22%3A12%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A65895%2C%22regionType%22%3A7%7D%5D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22sort%22%3A%7B%22value%22%3A%22globalrelevanceex%22%7D%7D%2C%22isListVisible%22%3Atrue%7D'
        url = 'https://www.zillow.com/homes/west-chester-pa_rb/'
        res = self.fetch(url)
        self.parse(res.text)
        time.sleep(2)
        self.getPageInfo()
        self.to_csv()

if __name__ == '__main__':
    scraper = ZillowScraper()
    scraper.run()
