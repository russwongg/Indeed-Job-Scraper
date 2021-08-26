import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import requests
import ssl
import time

'''
Singapore job scraper for Indeed.com.

WIP: how to track changes in jobs? and email the changes to yourself... watchdog?
'''

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def get_urls():
    search_list = []
    url_list = []

    job_search_criteria = input('Enter the job title that you want to search: ')
    search_list.append(job_search_criteria)
    # country = input('Enter job location: ')

    while True:
        option = input('Search another job (Y/N)? ')
        if len(option) < 1: break
        if option.lower() == 'y':
            job_search_criteria = input('Enter job title that you want to search: ')
            if len(job_search_criteria) < 1: break
            search_list.append(job_search_criteria)
        else:
            break

    print(f'Retrieving jobs for {search_list}')
    url_endpoint = 'https://sg.indeed.com/jobs?q='

    for search in search_list:
        word_list = search.split()
        index = 0
        while index < (len(word_list)):
            if index == 0:
                url = url_endpoint + word_list[index]
                index += 1
            elif index == (len(word_list) -1):
                url = url + '+' + word_list[index] + '&l=singapore&radius=10&fromage=3'
                index += 1
            else:
                url = url + '+' + word_list[index]
                index += 1
        url_list.append(url)

    # print(url_list)
    return url_list

def job_search(list_of_urls):
    # Search fixed income jobs from the last 3 days
    url_list = list_of_urls

    # helper functions
    def get_job_title(job):
        for span in job.find_all('span'):
            if span.get('title') is not None:
                return span.get('title')

    def get_company_name(job):
        for span in job.find_all('span', class_ = 'companyName'):
            if span is not None:
                return span.text

    for url in url_list:
        print('====Retrieving', url, 'jobs====\n')
        html = requests.get(url).text
        soup = BeautifulSoup(html, 'lxml')
        jobs = soup.find_all('div', class_ = 'slider_container')

        job_list = []
        # Retrieve jobs

        for index, job in enumerate(jobs, start = 1):

            job_title = get_job_title(job)
            company_name = get_company_name(job)

            if job not in job_list:
                job_list.append(job_title)
                print('Job', index)
                print('Job title:', job_title)
                print('Company name:', company_name)
                print('Posted:', job.find('span', class_ = 'date').text)
                print('Description:', job.find('div', class_ = 'job-snippet').text[:100])
                print('\n')
            else:
                print('===== New jobs ====')
                continue

if __name__ == '__main__':
    while True:
        # get_urls()

        job_search(get_urls())
        # how many minutes to wait?
        wait = 240
        print(f'Waiting {wait/60} hours')
        time.sleep(wait * 60)

        # how to compare one output against the first and return differences?
