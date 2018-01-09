from django.http import HttpResponse
from django.shortcuts import render
from bingScraper import models, exclude
import requests
from google import search
import pandas as pd
import os,io
import time, random, re, datetime
from django.shortcuts import render

# Create your views here.
def googleScraper(request):
    return render(request, 'googleScraper/googleScraper.html')

def scraping(request):
    if request.method == 'GET':
        return render(request, 'googleScraper/googleScraper.html')
    elif request.method == 'POST':
        print('loading data...')
        team = request.POST.get('team_select')
        extra = request.POST.get('true_or_false')
        keywords = request.POST.get('description')
        data = request.FILES['data']
        data = pd.read_excel(data)
        print('data loading completed.')
        list1 = keywords.split(',')
        list2 = request.POST.getlist('states')
        number = int(request.POST.get('number'))
        file_name = team + ' ' + list1[0] + '.csv'
        log = open('/home/user/SFA_scraper/log.txt', 'a')
        log.write('googleScraper  ' + team + '  ' + keywords + '  ' + str(datetime.datetime.now()) + '  ' + 'number of urls: ' +  str(number) + '\n')
        log.close()
        if not os.path.exists('/Users/admin/Desktop/output/' + file_name):
            print ('Everything is good, start scraping:')
        else:
            pass
        list3 = []
        for i in range(len(list1)):
            for j in range(len(list2)):
                list3.append(list1[i] + ' ' + list2[j])
        exclude_term = exclude.exclude_term()
        i = 0
        res = []
        while i < len(list3):
            try:
                for url in search(list3[i], tld='com', lang='en', num=100, start=0, stop=number,
                                  pause=random.uniform(5.0, 30.0)):
                    r = re.compile(r"https?://(www\.)?")
                    url = r.sub('', url).strip().strip('/')
                    url = url.split('/')[0]
                    res.append(url)

                    if len(res) % 10 == 0:
                        print(list3[i] + ' number of urls scraped: ' + str(len(res)))

                i += 1
            except:
                print('IP got blocked, restarting...')
                time.sleep(1000)

        for i in range(len(res)):
                res[i] = res[i].replace('https://', '').replace('http://', '').replace('www.', '').replace(
                    '\xa0', '/')
                res[i] = res[i].split('/')[0]
        res = list(set(res))

        for x in range(len(res)):
            for y in exclude_term:
                if y in res[x]:
                    res[x] = 'this is a bad url!!!'

        res = [x for x in res if '.com' in x or '.us' in x or '.org' in x or '.biz' in x or '.net' in x]
        if extra == 'yes':
            print('pulling company names...')
            title = models.scraping_title(res)
            scraped_information = pd.DataFrame(pd.Series(title), columns=['scraped_information'])
            scraped_information['URLtrim'] = res
            result = data.merge(scraped_information, how='right', on='URLtrim')
        else:
            test = pd.DataFrame(pd.Series(res), columns=['URLtrim'])
            result = data.merge(test, how='right', on='URLtrim')
        url_list = result['URLtrim'].values.tolist()
        for i in range(len(url_list)):
            url_list[i] = 'http://' + url_list[i]
        result['url'] = url_list
        filename = "output.xlsx"
        excel_file = io.BytesIO()
        xlwriter = pd.ExcelWriter(excel_file, engine='xlsxwriter',options={'remove_timezone': True})
        result.to_excel(xlwriter, sheet_name=filename)
        xlwriter.save()
        xlwriter.close()
        excel_file.seek(0)
        response = HttpResponse(excel_file.read(),
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=output.xlsx'
        
        print ('scraping done')
        print('Bye')
        return response
#        path_d = '/Users/admin/Desktop/output/'
#        result.to_csv(os.path.join(path_d, file_name))
#        print('scraping done, output file path: ' + path_d)
#        print('Bye')
#        html = '<html><body><h1>scraping done</h1></body></html>'
#        return HttpResponse(html)
