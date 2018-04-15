# -*- coding:utf-8 -*-
import time
import logging
import os
import requests
import errno
from bs4 import BeautifulSoup

DEFAULT_DATA_PATH = os.path.abspath(os.path.join(
    os.path.dirname(__file__), 'SEC-Edgar-Data'))

_CIK_API_URI = 'http://www.sec.gov/cgi-bin/browse-edgar' \
       '?action=getcompany&CIK={s}&count=10&output=xml'

def run(ticker):
    t1 = time.time()

    cik = get_cik(ticker)

    filing_10K(ticker, cik, '20180101', 100)
    filing_10Q(ticker, cik, '20180101', 100)

    t2 = time.time()
    print ("Total Time taken: "),
    print (t2 - t1)

def make_directory(company_code, cik, priorto, filing_type):

    path = os.path.join(DEFAULT_DATA_PATH, company_code)

    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise

def save_in_directory(company_code, cik, priorto, doc_list,
    doc_name_list, filing_type):

    for j in range(len(doc_list)):
        base_url = doc_list[j]
        r = requests.get(base_url)
        data = str(r.text)
        path = os.path.join(DEFAULT_DATA_PATH, company_code, doc_name_list[j])

        with open(path, "w") as f:
            f.write(data)

def filing_10Q(company_code, cik, priorto, count):

    make_directory(company_code, cik, priorto, '10-Q')

    base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type=10-Q&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
    print ("started 10-Q " + str(company_code))
    r = requests.get(base_url)
    data = r.text

    doc_list, doc_name_list = create_document_list(data)

    print(doc_list)
    print(len(doc_list))

    try:
        save_in_directory(company_code, cik, priorto, doc_list, doc_name_list, '10-Q')
    except Exception as e:
        print (str(e))

    print ("Successfully downloaded all the files")


def filing_10K(company_code, cik, priorto, count):

    make_directory(company_code,cik, priorto, '10-K')


    base_url = "http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK="+str(cik)+"&type=10-K&dateb="+str(priorto)+"&owner=exclude&output=xml&count="+str(count)
    print(base_url)
    print ("started 10-K " + str(company_code))

    r = requests.get(base_url)
    data = r.text
    print(base_url)

    doc_list, doc_name_list = create_document_list(data)
    print(doc_list)
    print(len(doc_list))

    try:
        save_in_directory(company_code, cik, priorto, doc_list, doc_name_list, '10-K')
    except Exception as e:
        print (str(e))

    print ("Successfully downloaded all the files")

def create_document_list(data):

    soup = BeautifulSoup(data)

    link_list = list()

    for link in soup.find_all('filinghref'):
        url = link.string
        if link.string.split(".")[len(link.string.split("."))-1] == "htm":
            url += "l"
        link_list.append(url)
    link_list_final = link_list
    print ("Starting download....")

    doc_list = list()

    doc_name_list = list()

    for k in range(len(link_list_final)):
        soup = BeautifulSoup(requests.get(link_list_final[k]).text, 'html.parser')
        for td in soup.find_all('td'):
            if td.string == 'XBRL INSTANCE DOCUMENT':
                doc_list.append('https://www.sec.gov' + str(td.parent.a.get('href')))
                doc_name_list.append(str(td.parent.a.get('href')).split('/')[-1])
    return doc_list, doc_name_list

def get_cik(symbol):

    response = requests.get(_CIK_API_URI.format(s=symbol))
    page_data = BeautifulSoup(response.text, "html.parser")
    cik = page_data.companyinfo.cik.string
    return cik

ticker = ['AAL', 'AAPL', 'ADBE', 'ADI', 'ADP', 'ADSK', 'AKAM', 'ALXN', 'AMAT', 'AMD', 'AMGN', 'AMZN', 'ATVI', 'AVGO', 'BBBY', 'BIIB', 'CA', 'CBOE', 'CELG', 'CERN', 'CHRW', 'CHTR', 'CINF', 'CMCSA', 'CME', 'COST', 'CSCO', 'CSX', 'CTAS', 'CTSH', 'CTXS', 'DISCA', 'DISCK', 'DISH', 'DLTR', 'EA', 'EBAY', 'EQIX', 'ESRX', 'ETFC', 'EXPD', 'EXPE', 'FAST', 'FB', 'FFIV', 'FISV', 'FITB', 'FLIR', 'FOX', 'FOXA', 'GILD', 'GOOG', 'GOOGL', 'GRMN', 'GT', 'HAS', 'HBAN', 'HOLX', 'HSIC', 'IDXX', 'ILMN', 'INCY', 'INFO', 'INTC', 'INTU', 'ISRG', 'JBHT', 'KHC', 'KLAC', 'LKQ', 'LRCX', 'MAR', 'MAT', 'MCHP', 'MDLZ', 'MNST', 'MSFT', 'MU', 'MYL', 'NAVI', 'NDAQ', 'NFLX', 'NTAP', 'NTRS', 'NVDA', 'NWS', 'NWSA', 'ORLY', 'PAYX', 'PBCT', 'PCAR', 'PCLN', 'PDCO', 'PYPL', 'QCOM', 'QRVO', 'REGN', 'ROST', 'SBUX', 'SNI', 'SNPS', 'SPLS', 'SRCL', 'STX', 'SWKS', 'SYMC', 'TRIP', 'TROW', 'TSCO', 'TXN', 'ULTA', 'VIAB', 'VRSK', 'VRSN', 'VRTX', 'WBA', 'WDC', 'WFM', 'WLTW', 'WYNN', 'XLNX', 'XRAY', 'ZION', 'A', 'AAP', 'ABBV', 'ABC', 'ABT', 'ACN', 'ADM', 'ADS', 'AEE', 'AEP', 'AES', 'AET', 'AFL', 'AGN', 'AIG', 'AIV', 'AIZ', 'AJG', 'ALB', 'ALK', 'ALL', 'ALLE', 'AME', 'AMG', 'AMP', 'AMT', 'AN', 'ANTM', 'AON', 'APA', 'APC', 'APD', 'APH', 'ARE', 'ARNC', 'AVB', 'AVY', 'AWK', 'AXP', 'AYI', 'AZO', 'BA', 'BAC', 'BAX', 'BBT', 'BBY', 'BCR', 'BDX', 'BEN', 'BF', 'BHI', 'BK', 'BLK', 'BLL', 'BMY', 'BRK', 'BSX', 'BWA', 'BXP', 'C', 'CAG', 'CAH', 'CAT', 'CB', 'CBG', 'CBS', 'CCI', 'CCL', 'CF', 'CFG', 'CHD', 'CHK', 'CI', 'CL', 'CLX', 'CMA', 'CMG', 'CMI', 'CMS', 'CNC', 'CNP', 'COF', 'COG', 'COH', 'COL', 'COO', 'COP', 'COTY', 'CPB', 'CRM', 'CSRA', 'CTL', 'CVS', 'CVX', 'CXO', 'D', 'DAL', 'DD', 'DE', 'DFS', 'DG', 'DGX', 'DHI', 'DHR', 'DIS', 'DLPH', 'DLR', 'DOV', 'DOW', 'DPS', 'DRI', 'DTE', 'DUK', 'DVA', 'DVN', 'DXC', 'ECL', 'ED', 'EFX', 'EIX', 'EL', 'EMN', 'EMR', 'EOG', 'EQR', 'EQT', 'ES', 'ESS', 'ETN', 'ETR', 'EVHC', 'EW', 'EXC', 'EXR', 'F', 'FBHS', 'FCX', 'FDX', 'FE', 'FIS', 'FL', 'FLR', 'FLS', 'FMC', 'FRT', 'FTI', 'FTV', 'GD', 'GE', 'GGP', 'GIS', 'GLW', 'GM', 'GPC', 'GPN', 'GPS', 'GS', 'GWW', 'HAL', 'HBI', 'HCA', 'HCN', 'HCP', 'HD', 'HES', 'HIG', 'HOG', 'HON', 'HP', 'HPE', 'HPQ', 'HRB', 'HRL', 'HRS', 'HST', 'HSY', 'HUM', 'IBM', 'ICE', 'IFF', 'IP', 'IPG', 'IR', 'IRM', 'IT', 'ITW', 'IVZ', 'JCI', 'JEC', 'JNJ', 'JNPR', 'JPM', 'JWN', 'K', 'KEY', 'KIM', 'KMB', 'KMI', 'KMX', 'KO', 'KORS', 'KR', 'KSS', 'KSU', 'L', 'LB', 'LEG', 'LEN', 'LH', 'LLL', 'LLY', 'LMT', 'LNC', 'LNT', 'LOW', 'LUK', 'LUV', 'LVLT', 'LYB', 'M', 'MA', 'MAA', 'MAC', 'MAS', 'MCD', 'MCK', 'MCO', 'MDT', 'MET', 'MHK', 'MKC', 'MLM', 'MMC', 'MMM', 'MNK', 'MO', 'MON', 'MOS', 'MPC', 'MRK', 'MRO', 'MS', 'MSI', 'MTB', 'MUR', 'NBL', 'NEE', 'NEM', 'NFX', 'NI', 'NKE', 'NLSN', 'NOC', 'NOV', 'NRG', 'NSC', 'NUE', 'NWL', 'O', 'OKE', 'OMC', 'ORCL', 'OXY', 'PCG', 'PEG', 'PEP', 'PFE', 'PFG', 'PG', 'PGR', 'PH', 'PHM', 'PKI', 'PLD', 'PM', 'PNC', 'PNR', 'PNW', 'PPG', 'PPL', 'PRGO', 'PRU', 'PSA', 'PSX', 'PVH', 'PWR', 'PX', 'PXD', 'RAI', 'RCL', 'REG', 'RF', 'RHI', 'RHT', 'RIG', 'RJF', 'RL', 'ROK', 'ROP', 'RRC', 'RSG', 'RTN', 'SCG', 'SCHW', 'SEE', 'SHW', 'SIG', 'SJM', 'SLB', 'SLG', 'SNA', 'SO', 'SPG', 'SPGI', 'SRE', 'STI', 'STT', 'STZ', 'SWK', 'SYF', 'SYK', 'SYY', 'T', 'TAP', 'TDG', 'TEL', 'TGT', 'TIF', 'TJX', 'TMK', 'TMO', 'TRV', 'TSN', 'TSO', 'TSS', 'TWX', 'TXT', 'UA', 'UAA', 'UAL', 'UDR', 'UHS', 'UNH', 'UNM', 'UNP', 'UPS', 'URI', 'USB', 'UTX', 'V', 'VAR', 'VFC', 'VLO', 'VMC', 'VNO', 'VTR', 'VZ', 'WAT', 'WEC', 'WFC', 'WHR', 'WM', 'WMB', 'WMT', 'WRK', 'WU', 'WY', 'WYN', 'XEC', 'XEL', 'XL', 'XOM', 'XRX', 'XYL', 'YUM', 'ZBH', 'ZTS']


for i in ticker:
    run(i)
