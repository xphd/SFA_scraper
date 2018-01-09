
from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,  related_name="profile")
    access_level = models.CharField(max_length=20, blank=True)
    team = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.access_level



# Create your models here.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import os
import sys
import re
import random

from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from pyvirtualdisplay import Display

def bing_grab(list1, list2, pages):
    list3 = []
    res = []
    for i in range(len(list1)):
        for j in range(len(list2)):
            list3.append(list1[i] + ' ' + list2[j])
    print(list3)

    
    # driver_path = ('C:\\Users\\admin\\SFA_scraper\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    # driver_path = ('/home/ubuntu/workspace/SFA_scraper/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    #b_path = os.path.join(BASE_DIR, 'bin/firefox/firefox')
    #binary = FirefoxBinary(b_path)
    #driver = webdriver.Firefox(firefox_binary=binary)
    #display = Display(visible=0, size=(800, 600))
    #display.start()
    
    
    file_name = 'bin/geckodriver'

#     file_name = 'bin/chromedriver'
    #path = '/home/alex/SFA_scraper/bin/geckodriver'
    path = os.path.join(BASE_DIR, file_name)
    #log_path = os.path.join(BASE_DIR, 'bin/geckodriver.log')
    log_path = os.path.join(BASE_DIR, 'bin/googledriver.log')
    driver = webdriver.Firefox(log_path = log_path, executable_path=path)
#     driver = webdriver.Chrome(executable_path=path)

    #WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_xpath("//*[@id='sb_form_q']"))
    #BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # file_name ="phantomjs-2.1.1-linux-x86_64/bin/phantomjs"
    # print(os.path.join(BASE_DIR, file_name))
    # driver = webdriver.phantomjs(os.path.join(BASE_DIR, file_name))

    
    # driver = webdriver.PhantomJS('/home/ubuntu/workspace/SFA_scraper/phantomjs-2.1.1-linux-x86_64/bin/phantomjs')
    base_url = 'https://www.bing.com/'

    driver.get(base_url)
    
    for i in range(len(list3)):
        driver.find_element_by_xpath("//*[@id='sb_form_q']").clear()
        # print (str(len(result)) + ' urls in output set')
        driver.find_element_by_xpath("//*[@id='sb_form_q']").send_keys(list3[i])
        driver.find_element_by_xpath("//*[@id='sb_form_go']").click()
        for k in range(1, pages+1):
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            links = soup.findAll('cite')
            for j in range(len(links)):
                links[j] = re.sub('<[^<]+?>', '', str(links[j]))
                res.append(links[j])
            print(list3[i] + ' number of urls scraped: ' + str(len(res)))
            if k == pages:
                break
            try:
                WebDriverWait(driver, 20).until(lambda driver: driver.find_element_by_class_name('sb_pagN'))
                driver.find_element_by_class_name('sb_pagN').click()
            except:
                break
            time.sleep(1)

    return res

def scraping_title(urls):
    title = []
    for url in urls:
        url = 'http://' + url
        if len(title)%10 == 0:
            print (str(len(title)) + ' companies name pulled.')
        try:
            html = requests.get(url, timeout = 10).text
            soup = BeautifulSoup(html, 'html.parser')
            title.append(soup.find('title').find(text=True))
        except:
            title.append('')

    return title

