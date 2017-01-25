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
