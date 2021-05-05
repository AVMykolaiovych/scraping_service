import requests
from bs4 import BeautifulSoup as BS
from random import randint


__all__ = ('work', 'rabota', 'dou', 'djinni')

headers = [
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'},
    {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:53.0) Gecko/20100101 Firefox/53.0',
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
    ]


def work(url):
    domain = 'https://www.work.ua'
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers[randint(0, 2)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='pjax-job-list')
        if main_div:
            div_lst = main_div.find_all('div', attrs={'class': 'job-link'})
            for div in div_lst:
                title = div.find('h2')
                href = title.a['href']
                content = div.p.text
                company = 'No name'
                logo = div.find('img')
                if logo:
                    company = logo['alt']
                jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists!'})
    else:
        errors.append({'url': url, 'title': 'Page does not answer!'})

    return jobs, errors


def rabota(url):
    domain = 'https://rabota.ua'
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers[randint(0, 2)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        avaliable_jobs = soup.find('div', attrs={'class': 'f-vacancylist-newnotfound'})
        if not avaliable_jobs:
            table = soup.find('table', id='ctl00_content_vacancyList_gridList')
            if table:
                tr_list = table.find_all('tr', attrs={'id': True})
                for tr in tr_list:
                    wrapper = tr.find('div', attrs={'class': 'card-body'})
                    if wrapper:
                        title = wrapper.find('h2', attrs={'class': 'card-title'})
                        href = title.a['href']
                        content = wrapper.p.text
                        company = 'No name'
                        name = wrapper.find('p', attrs={'class': 'company-name'})
                        if name:
                            company = name.a.text
                        jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
            else:
                errors.append({'url': url, 'title': 'Table does not exists!'})
        else:
            errors.append({'url': url, 'title': 'This page is empty!'})
    else:
        errors.append({'url': url, 'title': 'Page does not answer!'})

    return jobs, errors


def dou(url):
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers[randint(0, 2)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_div = soup.find('div', id='vacancyListId')
        if main_div:
            li_list = main_div.find_all('li', attrs={'class': 'l-vacancy'})
            for li in li_list:
                if '__hot' not in li['class']:
                    title = li.find('div', attrs={'class': 'title'})
                    href = title.a['href']
                    description = li.find('div', attrs={'class': 'sh-info'})
                    content = description.text
                    company = 'No name'
                    logo = title.find('a', attrs={'class': 'company'})
                    if logo:
                        company = logo.text
                    jobs.append({'title': title.text, 'url': href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists!'})
    else:
        errors.append({'url': url, 'title': 'Page does not answer!'})

    return jobs, errors


def djinni(url):
    domain = 'https://djinni.co'
    jobs = []
    errors = []
    resp = requests.get(url, headers=headers[randint(0, 2)])
    if resp.status_code == 200:
        soup = BS(resp.content, 'html.parser')
        main_ul = soup.find('ul', attrs={'class': 'list-jobs'})
        if main_ul:
            li_list = main_ul.find_all('li', attrs={'class': 'list-jobs__item'})
            for li in li_list:
                title = li.find('div', attrs={'class': 'list-jobs__title'})
                href = title.a['href']
                description = li.find('div', attrs={'class': 'list-jobs__description'})
                content = description.p.text
                company = 'No name'
                details = li.find('div', attrs={'class': 'list-jobs__details'})
                logo = details.find('a', attrs={'style': True})
                if logo:
                    company = logo.text
                jobs.append({'title': title.text, 'url': domain + href, 'description': content, 'company': company})
        else:
            errors.append({'url': url, 'title': 'Div does not exists!'})
    else:
        errors.append({'url': url, 'title': 'Page does not answer!'})

    return jobs, errors
