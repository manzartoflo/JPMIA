#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 22:04:56 2019

@author: manzars
"""

from selenium import webdriver
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import time
url = "http://www.jpmia.gr.jp/member/"
wb = webdriver.Chrome("/home/manzars/Downloads/chromedriver")
wb.get(url)
html = wb.execute_script('return document.documentElement.outerHTML')
soup = BeautifulSoup(html, 'lxml')
table = soup.findAll('table')
tds = table[0].findAll('td')
links = []
for td in tds:
    try:
        link = td.a.attrs['href'].split("Window('")[1].split("',")[0]
        links.append(urljoin(url, link))
    except:
        pass
tels = []
emails = []
urls = []
for link in links:
    wb.get(link)
    #time.sleep(1)
    html = wb.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'lxml')
    table = soup.findAll('table')
    tds = table[4].findAll('td')
    tds = tds[1::2]
    try:
        tel = tds[1].text.split('TEL：')[1]
    except:
        tel = "NaN"
    
    tel = tel.replace('\n', '').lstrip()
    try:
        tel = tel.split('FAX')[0]
    except:
        pass
    
    try:
        tel = tel.split('　（総務人事グループ）')[0]
    except:
        pass
    print(tel)
    try:
        url = tds[0].a.attrs['href']
    except:
        url = 'NaN'
    
    #print(url)
    
    try:
        email = tds[-1].a.attrs['href'].split('mailto:')[1]
    except:
        email = 'NaN'
    tels.append(tel)
    emails.append(email)
    urls.append(url)
    
    #print(email)
wb.close()
prefs = {
  "translate_whitelists": {"fr":"en"},
  "translate":{"enabled":"true"}
}
url = "http://www.jpmia.gr.jp/member/"
options = webdriver.ChromeOptions()
options.add_experimental_option('prefs', prefs)
wb = webdriver.Chrome("/home/manzars/Downloads/chromedriver", chrome_options=options)
wb.get(url)
html = wb.execute_script('return document.documentElement.outerHTML')
soup = BeautifulSoup(html, 'lxml')
table = soup.findAll('table')
tds = table[0].findAll('td')
links = []
for td in tds:
    try:
        link = td.a.attrs['href'].split("Window('")[1].split("',")[0]
        links.append(urljoin(url, link))
    except:
        pass
names = []
for link in links:
    wb.get(link)
    time.sleep(3)
    html = wb.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'lxml')
    name = soup.findAll('b')
    name = name[0].text
    names.append(name)

header = "Company name, Telephone, Email, Website\n"
file = open('assignment.csv', 'w')
file.write(header)
for i in range(len(names)):
    file.write(names[i].replace(',', '') + ', ' + tels[i].replace(',', '') + ', ' + emails[i] + ', ' + urls[i] + '\n')
file.close()
wb.close()    