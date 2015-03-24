import os
import sys
import logging

import requests
from bs4 import BeautifulSoup

FOIA_REQUEST_URL_BASE = 'https://foiaonline.regulations.gov'
FOIA_REQUEST_URL_REQUEST_PAGE = '/foia/action/public/view/request?objectId='
FOIA_REQUEST_URL_PAGE_QUERY = '&event=request&d-8138531-p='
FOIA_REQUEST_PAGE_SIZE = 50

def index(request_id, index_file):
    print 'Writing file index to ' + index_file
    f = open(index_file, 'w')

    print 'Downloading index...'
    page_1 = requests.get(FOIA_REQUEST_URL_BASE + FOIA_REQUEST_URL_REQUEST_PAGE + str(request_id))
    page_1_soup = BeautifulSoup(page_1.text)
    num_records_statement = page_1_soup.find_all('div', class_='subHeaderLeft')[2].get_text()
    num_records = int(num_records_statement.split(' ')[0].replace(',', ''))
    num_pages = int(num_records / float(FOIA_REQUEST_PAGE_SIZE)) + 1
    print (str(num_records) + ' found on ' + str(num_pages) + ' pages.')

    print 'Analyzing file list...'
    for page_num in range(1, num_pages):
        print ('  Page ' + str(page_num) + ' of ' + str(num_pages))
        page = requests.get(FOIA_REQUEST_URL_BASE + str(request_id) +
                            FOIA_REQUEST_URL_PAGE_QUERY + str(page_num))
        page_soup = BeautifulSoup(page.text)
        links = page_soup.select('#dttPubRecords td a')
        for link in links:
            f.write(link.get_text() + ',' + link['href'] + '\n')
    print 'All results written to ' + index_file
    index_file.close()

def download(request_id, index_file):
    print 'Reading from ' + index_file
    index_file = open(index_file, 'r')
    for line in index_file:
        contents = line.split(',')
        file_name = contents[0]
        page_url = contents[1]
        page = requests.get(FOIA_REQUEST_URL_BASE + page_url)
        page_soup = BeautifulSoup(page.text)
        file_url = page_soup.select('form#mainForm fieldset .subContentFull a')[0]['href']
        file_format = 'pdf'  # NOTE: Assuming all PDFs

        print '  Downloading ' + file_name + '...'
        download = requests.get(FOIA_REQUEST_URL_BASE + file_url)
        file = open(file_name + '.' + file_format, 'wb')
        file.write(download.content)
        file.close()
    print 'All files downloaded.'
    index_file.close()

if __name__ == "__main__":
    request_id = sys.argv[1]
    index_file = 'foia-index.txt'
    index(request_id, index_file)
    download(request_id, index_file)
