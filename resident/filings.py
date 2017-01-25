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
    print(information.tag)
    info = []
    shrsOrPrnAmt = []
    voting_authority = []

    '''setting up the head'''
    # if count == 0:
    #     name_of_issuer = information.find('nameOfIssuer').tag
    #     filings_head.append(name_of_issuer)
    #     title_of_class = information.find('titleOfClass').tag
    #     filings_head.append(title_of_class)
    #     cusip = information.find('cusip').tag
    #     filings_head.append(cusip)
    #     value = information.find('value').tag
    #     filings_head.append(value)
    #     shrs_or_prn_amt = information.find('shrsOrPrnAmt').tag
    #     filings_head.append(shrs_or_prn_amt)
    #     investment_discretion = information.find('investmentDiscretion').tag
    #     filings_head.append(investment_discretion)
    #     voting_authority = information.find('votingAuthority').tag
    #     filings_head.append(voting_authority)
    #     csvwriter.writerow(filings_head)
    #     count = count + 1

    '''parse through xml for data values'''
    # name_of_issuer = information.find('nameOfIssuer').text
    # info.append(name_of_issuer)
    # title_of_class = information.find('titleOfClass').text
    # info.append(title_of_class)
    # cusip = information.find('cusip').text
    # info.append(cusip)
    # value = information.find('value').text
    # info.append(value)
    # investment_discretion = information.find('investmentDiscretion').text
    # info.append(investment_discretion)
    # voting_authority = information.find('votingAuthority').text
    # info.append(voting_authority)
    # csvwriter.writerow(filings_head)
    # count = count + 1


filings_data.close()
