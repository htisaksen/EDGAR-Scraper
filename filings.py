import xml.etree.ElementTree as ET
import csv
import re


tree = ET.parse("filings.xml")
root = tree.getroot()
# open a file for writing

filings_data = open('./filingsdata.csv', 'w')

#cleans URI namehead from tag
def xmlns_remove(string):
    return string.replace(xmlns,'')

# create the csv writer object

csvwriter = csv.writer(filings_data)


filings_head = []
count = 0
for information in root.findall('./*'):
    xmlns = '{http://www.sec.gov/edgar/document/thirteenf/informationtable}'
    info = []
    shrsOrPrnAmt = []
    voting_authority_list = []

    '''setting up the head'''
    if count == 0:
        name_of_issuer =  xmlns_remove(information.find(xmlns+'nameOfIssuer').tag)
        filings_head.append(name_of_issuer)
        title_of_class = xmlns_remove(information.find(xmlns+'titleOfClass').tag)
        filings_head.append(title_of_class)
        cusip = xmlns_remove(information.find(xmlns+'cusip').tag)
        filings_head.append(cusip)
        value = xmlns_remove(information.find(xmlns+'value').tag)
        filings_head.append(value)
        shrs_or_prn_amt = xmlns_remove(information.find(xmlns+'shrsOrPrnAmt').tag)
        filings_head.append(shrs_or_prn_amt)
        investment_discretion = xmlns_remove(information.find(xmlns+'investmentDiscretion').tag)
        filings_head.append(investment_discretion)
        voting_authority = xmlns_remove(information.find(xmlns+'votingAuthority').tag)
        filings_head.append(voting_authority)
        csvwriter.writerow(filings_head)
        count = count + 1

    print(information[4][0].text)
    '''parse through xml for data values'''
    name_of_issuer = information.find(xmlns+'nameOfIssuer').text
    info.append(name_of_issuer)
    title_of_class = information.find(xmlns+'titleOfClass').text
    info.append(title_of_class)
    cusip = information.find(xmlns+'cusip').text
    info.append(cusip)
    value = information.find(xmlns+'value').text
    info.append(value)
    sshPrnamt = information[4][0].text
    shrsOrPrnAmt.append(sshPrnamt)
    sshPrnamtType = information[4][1].text
    shrsOrPrnAmt.append(sshPrnamtType)
    info.append(shrsOrPrnAmt)
    investment_discretion = information.find(xmlns+'investmentDiscretion').text
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
