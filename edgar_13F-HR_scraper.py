import requests
import re
import xml.etree.ElementTree as ET
import csv
from lxml.html.soupparser import fromstring
from bs4 import BeautifulSoup

notxml = 'https://www.sec.gov/Archives/edgar/data/1166559/000104746907006532/0001047469-07-006532.txt'
isxml = 'https://www.sec.gov/Archives/edgar/data/1166559/000110465914039387/0001104659-14-039387.txt'
sample_route = 'https://www.sec.gov/Archives/edgar/data/1166559/000110465914039387/0001104659-14-039387.txt'

class Scraper():

    def __init__(self,ticker_or_cik):
        self.ticker_or_cik = ticker_or_cik
        self.url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker_or_cik}&type=13F-HR&dateb=&owner=exclude&count=100&output=atom'.format(ticker_or_cik=self.ticker_or_cik)
        self.links = self.find_links()

        '''function calls to automate scrape process'''
        self.compile_filings()

    '''retrieves xml with url var. Formatted for 13-HR form'''
    def get_xml(self,url):
        response = requests.get(url)
        soup_text = BeautifulSoup(response.text,'xml')
        return soup_text

    '''Parses through self.url for links to all of the filings for the given organization'''
    def find_links(self):
        meta = self.get_xml(self.url)
        links = []
        for link in meta.find_all('filing-href'):
            link = link.get_text()
            link = link.replace('-index.htm','.txt')
            links.append(link)
        return links

    '''checks format of link and passes it through respective parser for transformation'''
    def compile_filings(self):
        for link in self.links:
            if self.check_if_xml:
                self.parse_deliminate_xml(link)

    '''Checks to see format of the url. Returns a boolean(SEC-DOCUMENT will signify XML formats)'''
    def check_if_xml(self,url):
        format_check = requests.get(url)
        if format_check.text[1:13] == 'SEC-DOCUMENT':
            return True
        else:
            return False

    '''creates csv from xml'''
    def parse_deliminate_xml(self,url):

        xml_string = str(self.get_xml(url))

        '''using regex to group segments of the txt/string'''
        xml_string_start = re.finditer(r"<XML>", xml_string)
        xml_string_close = re.finditer(r"</XML>", xml_string)


        start_index = [i.start()+len("<XML>\n") for i in xml_string_start]
        close_index = [i.start() for i in xml_string_close]


        '''Meta info provides information about the filing and information table segments the tags to transform into CSV format'''
        #meta_info = xml_string[start_index[0]:close_index[0]]
        information_table = xml_string[start_index[1]:close_index[1]]

        root = fromstring(information_table)
        '''writing csv to filingsdata.csv'''
        filing_id = url[-20:-4]
        filings_data = open('./{filing_id}-13F-HR-Filing.csv'.format(filing_id = filing_id), 'w')
        csvwriter = csv.writer(filings_data, delimiter = '\t')

        filings_head = []
        count = 0
        for information in root.findall('.//infotable'):
            info = []
            shrsOrPrnAmt = []
            voting_authority_list = []

            '''Finding tag values to use for the head'''
            if count == 0:
                name_of_issuer =  information.find('nameofissuer').tag
                filings_head.append(name_of_issuer)
                title_of_class = information.find('titleofclass').tag
                filings_head.append(title_of_class)
                cusip = information.find('cusip').tag
                filings_head.append(cusip)
                value = information.find('value').tag
                filings_head.append(value)
                shrs_or_prn_amt = information.find('shrsorprnamt').tag
                filings_head.append(shrs_or_prn_amt)
                investment_discretion = information.find('investmentdiscretion').tag
                filings_head.append(investment_discretion)
                voting_authority = information.find('votingauthority').tag
                filings_head.append(voting_authority)
                csvwriter.writerow(filings_head)
                count = count + 1

            '''parse through xml for data text'''
            name_of_issuer = information.find('nameofissuer').text
            info.append(name_of_issuer)
            title_of_class = information.find('titleofclass').text
            info.append(title_of_class)
            cusip = information.find('cusip').text
            info.append(cusip)
            value = information.find('value').text
            info.append(value)
            sshPrnamt = information[4][0].text
            shrsOrPrnAmt.append(sshPrnamt)
            sshPrnamtType = information[4][1].text
            shrsOrPrnAmt.append(sshPrnamtType)
            info.append(shrsOrPrnAmt)
            investment_discretion = information.find('investmentdiscretion').text
            info.append(investment_discretion)
            sole = information[6][0].text
            voting_authority_list.append(sole)
            shared = information[6][1].text
            voting_authority_list.append(shared)
            none = information[6][2].text
            voting_authority_list.append(none)
            info.append(voting_authority_list)
            csvwriter.writerow(info)
            count = count + 1

        filings_data.close()

if __name__=="__main__":
    organization = Scraper('0001166559')
