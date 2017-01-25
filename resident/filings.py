import xml.etree.ElementTree as ET
import csv
import re

tree = ET.parse("filings.txt")
root = tree.getroot()
# open a file for writing

filings_data = open('./filingsdata.csv', 'w')

# create the csv writer object

csvwriter = csv.writer(filings_data)
filings_head = []
count = 0

for information in root.findall('./*'):
    xmlns = '{http://www.sec.gov/edgar/document/thirteenf/informationtable}'
    info = []
    shrsOrPrnAmt = []
    voting_authority = []

    '''setting up the head'''
    if count == 0:
        name_of_issuer = information.find(xmlns+'nameOfIssuer').tag
        filings_head.append(name_of_issuer)
        title_of_class = information.find(xmlns+'titleOfClass').tag
        filings_head.append(title_of_class)
        cusip = information.find(xmlns+'cusip').tag
        filings_head.append(cusip)
        value = information.find(xmlns+'value').tag
        filings_head.append(value)
        shrs_or_prn_amt = information.find(xmlns+'shrsOrPrnAmt').tag
        filings_head.append(shrs_or_prn_amt)
        investment_discretion = information.find(xmlns+'investmentDiscretion').tag
        filings_head.append(investment_discretion)
        voting_authority = information.find(xmlns+'votingAuthority').tag
        filings_head.append(voting_authority)
        csvwriter.writerow(filings_head)
        count = count + 1

    '''parse through xml for data values'''
    # name_of_issuer = information.find(xmlns+'nameOfIssuer').text
    # info.append(name_of_issuer)
    # title_of_class = information.find(xmlns+'titleOfClass').text
    # info.append(title_of_class)
    # cusip = information.find(xmlns+'cusip').text
    # info.append(cusip)
    # value = information.find(xmlns+'value').text
    # info.append(value)
    # investment_discretion = information.find(xmlns+'investmentDiscretion').text
    # info.append(investment_discretion)
    # voting_authority = information.find(xmlns+'votingAuthority').text
    # info.append(voting_authority)
    # csvwriter.writerow(filings_head)
    # count = count + 1


filings_data.close()
