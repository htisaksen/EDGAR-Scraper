import requests
import re
import xml.etree.ElementTree as ET
import csv
import os
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

    '''retrieves xml with url var. Formatted for 13-HR form. Pass in xml or html as a string for second parameter'''
    def get_url(self,url,format_type):

        response = requests.get(url)

        if format_type == 'xml':
            soup_text = BeautifulSoup(response.text,'xml')
            return soup_text
        if format_type == 'html':
            soup_text = BeautifulSoup(response.text,'html.parser')
            return soup_text
    def get_html(self,url):
        response = request.get(url)

    '''Parses through self.url for links to all of the filings for the given organization'''
    def find_links(self):
        meta = self.get_url(self.url,'xml')
        links = []
        for link in meta.find_all('filing-href'):
            link = link.get_text()
            link = link.replace('-index.htm','.txt')
            links.append(link)
        return links

    '''checks format of link and passes it through respective parser for transformation. Will add try and catch to provide validation on check'''
    def compile_filings(self):
        print(self.links)
        for link in self.links:
            print(type(link))
            if self.check_if_xml(link):
                print('xml')
                self.parse_deliminate_xml(link)
            else:
                print('html')
                self.parse_deliminate_html(link)
    '''Checks to see format of the url. Returns a boolean(SEC-DOCUMENT will signify XML formats) True: XML False: Text'''
    def check_if_xml(self,url):
        response = requests.get(url)
        response_text = response.text
        #String is a unique tag in non xml format
        if '<DESCRIPTION>13F-HR' in response_text:
            return False
        else:
            return True

    '''parses and creates a CSV file with tab delimited values from html text'''
    def parse_deliminate_html(self,url):

        print(url)

        html_text = requests.get(url)
        html_text = html_text.text

        '''find the starting point of <S> to </Table> for all necessary information'''
        table_start = list(re.finditer(r'<S>',html_text))

        if len(list(re.finditer(r'</TABLE>',html_text))) == 0:
            table_end = list(re.finditer(r'</Table>',html_text))
        else:
            table_end = list(re.finditer(r'</TABLE>',html_text))

        table_start_index = [i.start()+len("<S>\n") for i in table_start]
        table_end_index = [i.start() for i in table_end]

        table_info = html_text[table_start_index[0]:table_end_index[0]]

        #use c_tag to indicate start of column
        c_tag = list(re.finditer(r"<C>", table_info))
        # create positions for the <C> tags
        c_tag_position = [c.start() for c in c_tag]
        #place 0 in c_tag_list for initial index
        c_tag_position.insert(0,0)

        '''hard coded headers for csv file'''
        csv_headers = ['nameofissuer','titleofclass','cusip','value','shrsorprnamt','investmentdiscretion','othermanagers','votingauthority']

        '''creates a dump file labeled the cik or ticker for CSV files naming is set to the name of the file'''
        if not os.path.exists(self.ticker_or_cik):
            os.makedirs(self.ticker_or_cik)
        filing_id = url[-20:-4]
        filings_data = open('./{ticker_or_cik}/{filing_id}-13F-HR-Filing.csv'.format(ticker_or_cik = self.ticker_or_cik,filing_id = filing_id), 'w')
        csvwriter = csv.writer(filings_data,delimiter = '\t')
        csvwriter.writerow(csv_headers)

        '''creating a list to write rows in csv'''
        for fundline in table_info.split('\n')[1:-1]:
            temp_list = []
            shrsorprnamt = []
            temp_list.append(fundline[c_tag_position[0]:c_tag_position[1]+4])           #nameofissuer
            temp_list.append(fundline[c_tag_position[1]+4:c_tag_position[2]+4])         #titleofclass
            temp_list.append(fundline[c_tag_position[2]:c_tag_position[3]+3])           #cusip
            temp_list.append(fundline[c_tag_position[3]+3:c_tag_position[4]+3])         #value
            shrsorprnamt.append(fundline[c_tag_position[4]+4:c_tag_position[5]+4])      #shrsorprnamt
            shrsorprnamt.append(fundline[c_tag_position[5]+1:c_tag_position[6]])        #sh/prn
            temp_list.append(shrsorprnamt)
            temp_list.append(fundline[c_tag_position[6]:c_tag_position[7]])             #investmentdiscretion
            temp_list.append(fundline[c_tag_position[7]:c_tag_position[8]])             #othermanagers
            temp_list.append(fundline[c_tag_position[8]:c_tag_position[9]])             #votingauthority
            temp_list.append(fundline[c_tag_position[9]:c_tag_position[10]+3])
            csvwriter.writerow(temp_list)

        filings_data.close()

    '''creates csv from xml'''
    def parse_deliminate_xml(self,url):

        xml_string = str(self.get_url(url,'xml'))

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

        if not os.path.exists(self.ticker_or_cik):
            os.makedirs(self.ticker_or_cik)

        filing_id = url[-20:-4]
        filings_data = open('./{ticker_or_cik}/{filing_id}-13F-HR-Filing.csv'.format(ticker_or_cik = self.ticker_or_cik,filing_id = filing_id), 'w')
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
