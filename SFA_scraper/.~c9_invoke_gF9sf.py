from django.http import HttpResponse
import io
from django.shortcuts import render, redirect
from . import models
import pandas as pd
from googleScraper.models import Company, CheckListLogs, UploadListLogs
from django.contrib.auth import login, authenticate
from .forms import SignUpForm, SignInForm, AddCompanyForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .decorators import user_is_manager, user_is_searcher
from django.contrib.auth.models import User
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
import time
import os
import sys
import re
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from pyvirtualdisplay import Display

import os

def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, 'main.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            form.save()
            form.save_profile()
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'main.html', {'user': user})
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'main.html', {'user': user})
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form})

@login_required(login_url = '/signin/')
def log_out(request):
    logout(request)
    return render(request, 'main.html')

@login_required(login_url = '/signin/')
def addCompany(request):
    if request.method == 'POST':
        form = AddCompanyForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'main.html', {'message': 'Add company successfully'})
    else:
        form = AddCompanyForm()
    return render(request, 'addCompany.html',{'form': form})

@login_required(login_url = '/signin/')
@user_is_manager
def upload(request):
    if request.method == 'POST':
        user = request.user
        fname = user.first_name
        lname = user.last_name
        team = user.profile.team
        try:
            data = request.FILES['override']
            input_name = data.name
            data = pd.read_excel(data)
            data['datetime'] = str(datetime.datetime.now())
            UploadListLogs.objects.create(datetime = str(datetime.datetime.now()), file_name = input_name, user_name = fname + ' ' + lname, team = team, upload_type = 'Override', file_length = data.shape[0])
            models.override_upload(data)
            return render(request, 'main.html', {'message': 'Upload list successfully'})
        except:
            data = request.FILES['passive']
            input_name = data.name
            data = pd.read_excel(data)
            data['datetime'] = str(datetime.datetime.now())
            UploadListLogs.objects.create(datetime=str(datetime.datetime.now()), file_name=input_name,
                                          user_name=fname + ' ' + lname, team=team, upload_type='Passive', file_length = data.shape[0])
            models.passive_upload(data)
            return render(request, 'main.html', {'message': 'Upload list successfully'})
    else:
        return render(request, 'upload.html')

@login_required(login_url = '/signin/')
def checklist(request):
    if request.method == 'POST':
        file = request.FILES['check_list']
        url_list = pd.DataFrame(pd.read_excel(file), columns=['url'])
        input_name = file.name
        user = request.user
        fname = user.first_name
        lname = user.last_name
        team = user.profile.team
        CheckListLogs.objects.create(datetime=str(datetime.datetime.now()), file_name=input_name,
                                          user_name=fname + ' ' + lname, team=team, status='Completed', file_length = url_list.shape[0])
        filename = 'output.xlsx'
        excel_file = io.BytesIO()
        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter',options={'remove_timezone': True})
        data = pd.DataFrame(list(Company.objects.all().values()))
        result = data.merge(url_list, how='right', on='url')
        result.to_excel(xlwriter, sheet_name=filename)
        xlwriter.save()
        xlwriter.close()
        excel_file.seek(0)
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=output.xlsx'
        return response
    else:
        return render(request, 'checklist.html')

@login_required(login_url = '/signin/')
def search_company(request):
    if request.method == 'POST':
        key = request.POST.get('search')
        keys = key.split()
        key = ' '.join(keys)
        company = list(set(list(Company.objects.filter(name__iexact=key)) + list(Company.objects.filter(name__icontains=key))))
        if len(company) > 10:
            company = company[:10]
        if len(company) == 0:
            company = Company.objects.filter(url=key)
            if len(company) == 0:
                return render(request, 'search_result.html', {'error': 'Cannot find company: ' + key})
            else:
                return render(request, 'search_result.html', {'company': company})
        else:
            return render(request, 'search_result.html', {'company': company})
    else:
        return render(request, 'main.html')

@login_required(login_url = '/signin/')
@user_is_manager
def user_management(request):
    users = User.objects.all()
    return render(request, 'user_management.html', {'users':users})

@login_required(login_url = '/signin/')
@user_is_manager
def view_logs(request):
    ckeck_logs = CheckListLogs.objects.all()
    upload_logs = UploadListLogs.objects.all()
    return render(request, 'activity_logs.html', {'check_logs': ckeck_logs,'upload_logs':upload_logs})

@login_required(login_url = '/signin/')
@user_is_manager
def change_user_info(request, user_id):
    if request.method == 'POST':
        new_access_level = request.POST.get('access_level')
        profile = User.objects.get(id=user_id).profile
        profile.access_level = new_access_level
        profile.save(update_fields=['access_level'])
        return render(request, 'main.html', {'message':'Update information successful!'})
    else:
        user = User.objects.get(id = user_id)
        return render(request, 'change_user_info.html', {'user':user})

@login_required(login_url = '/signin/')
@user_is_manager
def remove_user(request, user_id):
    User.objects.get(id = user_id).delete()
    return render(request, 'main.html', {'message':'Delete User successful!'})
    
@login_required(login_url = '/signin/')
def findCompany(request):
    if request.method == 'POST':
        info = request.POST.get('single_url')
        if info == None:
            info = request.FILES['list_urls']
            urls = pd.read_csv(info)['Website'].values.tolist()
            for i in range(len(urls)):
                urls[i] = urls[i].replace('http://', '')
            base_url = 'https://www.google.com/'
            
            
            display = Display(visible=0, size=(800, 600))
            display.start()
            driver = webdriver.Firefox()
            driver.get(base_url)
            WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_xpath("//*[@id='lst-ib']"))
            url_list = urls
            output = []
            for i in range(len(url_list)):
                url_list[i] = url_list[i].replace('http://', '')
                driver.find_element_by_xpath("//*[@id='lst-ib']").send_keys(url_list[i])
                time.sleep(random.uniform(1.0,5.0))
                try:
                    driver.find_element_by_xpath("//*[@id='_fZl']").click()
                except:
                    driver.close()
                    display = Display(visible=0, size=(800, 600))
                    display.start()
                    driver = webdriver.Firefox()
                    driver.get(base_url)
                    driver.find_element_by_xpath("//*[@id='lst-ib']").send_keys(url_list[i])
                    time.sleep(2)
                    driver.find_element_by_xpath("//*[@id='_fZl']").click()
                try:
                    WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_xpath("//*[@id='rhs_block']/div"))
                except:
                    output.append([url_list[i], ' ', ' ', ' ', ' ', ' ', ' '])
                    driver.get(base_url)
                    continue
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    name = soup.find('div',{'class': 'kno-ecr-pt kno-fb-ctx _hdf'}).find('span').find(text = True)
                except:
                    name = ''
                try:
                    address = soup.find('span', {'class': '_Xbe'}).find(text = True)
                except:
                    address = ''
                try:
                    web = soup.find('div', {'class': '_ldf'}).find('a')['href']
                except:
                    web = ''
                try:
                    phone = soup.find('span', {'data-dtype': 'd3ph'}).find('span').find(text = True)
                except:
                    phone = ''
                try:
                    city = address.split(', ')[1]
                except:
                    city = ''
                try:
                    state = address.split(', ')[2].split(' ')[0]
                except:
                    state = ''
                try:
                    zipcode = address.split(', ')[2].split(' ')[1]
                except:
                    zipcode = ''
                output.append([url_list[i], name, address, city, state, zipcode, web])
                time.sleep(random.uniform(1.0,5.0))
                print (len(output))
                driver.get(base_url)
            filename = 'output.xlsx'
            excel_file = io.BytesIO()
            xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter')
            result = pd.DataFrame(output, columns=['name', 'address','web','phone','city','state','zipcode'])
            # result.to_excel(xlwriter, sheet_name=filename)
            # xlwriter.save()
            # xlwriter.close()
            # excel_file.seek(0)
            # response = HttpResponse(excel_file.read(),
            #                         content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            # response['Content-Disposition'] = 'attachment; filename=output.xlsx'
            path_d = '/home/ubuntu/workspace/SFA_scraper/'
        
            result.to_csv(os.path.join(path_d, file_name))
            return response
        else:
            base_url = 'https://www.google.com/'
            display = Display(visible=0, size=(800, 600))
            display.start()
            driver = webdriver.Firefox()
            driver.get(base_url)
            WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_xpath("//*[@id='lst-ib']"))
            info = info.replace('http://', '')
            driver.find_element_by_xpath("//*[@id='lst-ib']").send_keys(info)
            time.sleep(random.uniform(1.0,5.0))
            driver.find_element_by_xpath("//*[@id='_fZl']").click()
            try:
                WebDriverWait(driver, 2).until(lambda driver: driver.find_element_by_xpath("//*[@id='rhs_block']/div"))
                html = driver.page_source
                soup = BeautifulSoup(html, 'html.parser')
                try:
                    name = soup.find('div',{'class': 'kno-ecr-pt kno-fb-ctx _hdf'}).find('span').find(text = True)
                except:
                    name = ''
                try:
                    address = soup.find('span', {'class': '_Xbe'}).find(text = True)
                except:
                    address = ''
                try:
                    web = soup.find('div', {'class': '_ldf'}).find('a')['href']
                except:
                    web = ''
                try:
                    phone = soup.find('span', {'data-dtype': 'd3ph'}).find('span').find(text = True)
                except:
                    phone = ''
                try:
                    city = address.split(', ')[1]
                except:
                    city = ''
                try:
                    state = address.split(', ')[2].split(' ')[0]
                except:
                    state = ''
                try:
                    zipcode = address.split(', ')[2].split(' ')[1]
                except:
                    zipcode = ''
                output = [info, name, address, city, state, zipcode, web]
            except:
                output = [info, ' ', ' ', ' ', ' ', ' ', ' ']
            return HttpResponse(str(output))
    else:
        return render(request, 'find_company.html')
    
    