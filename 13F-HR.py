import requests
import re
import xml.etree.ElementTree as ET
import csv
from bs4 import BeautifulSoup

#tree = ET.parse("resident_data.xml")
#root = tree.getroot()

#Write 13F-HR xml to CSV
info_required_filing = open('./info_required_filing.csv', 'w')
csvwriter = csv.writer(info_required_filing)

#Test variables
sample_route = 'https://www.sec.gov/Archives/edgar/data/1166559/000110465914039387/0001104659-14-039387.txt'
company_ciknum = 'GOOG'
url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='+ company_ciknum +'&type=&dateb=&owner=exclude&count=100'

class Scraper():

    def __init__(self,ticker_OR_CIK):
        self.ticker_OR_CIK = ticker_OR_CIK

    def getXml(self,url):
        response = requests.get(url)
        soup_text = BeautifulSoup(response.text,'html.parser')
        return soup_text

    def parse_deliminate(self):
        #tree = ET.parse(getXml)
        #root = tree.getroot()
        pass

if __name__=="__main__":
    organization = Scraper('0001166559')
    print(organization.getXml(sample_route))
    print(organization.parse_deliminate())

# r= requests.get('http://www.investopedia.com/categories/bonds.asp')
#
# soup = BeautifulSoup(r.text, 'html.parser')
#
# item_title = [a['href'] for a in soup.find_all('a',attrs={'data-cat': 'content_list'})]
# print(item_title)
# print(type(item_title))
# frontdump=[]
# backdump=[]
# dictionary = {}
# for i in item_title:
#     time.sleep(.5)
#     r1=[]
#     r1 = requests.get('http://www.investopedia.com'+i)
#     soup=BeautifulSoup(r1.text, 'html.parser')
#     front=soup.find('h1').text
#     lasertarget=soup.find('div',attrs={'class': 'content-box content-box-term'}).find('p').text
#     back=re.match(r'[^\n]+',lasertarget).group()
#     frontdump.append(front)
#     backdump.append(back)
#
#
# dictionary = dict(zip(frontdump, backdump))
#
#
# with open('fixedincome.pkl', 'wb') as f:
#     pickle.dump(dictionary, f)
