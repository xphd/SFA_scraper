from django.http import HttpResponse
from django.shortcuts import render
from . import models, exclude
import requests
import pandas as pd
import os
import io, datetime, time
# Create your views here.
def bingScraper(request):
    return render(request, 'bingScraper/bingScraper.html')

def scraping(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'bingScraper/bingScraper.html')
    elif request.method == 'POST':
        # No need to call post.save() at this point -- it's already saved.
        # form = SearchForm(request.POST)
        # database = form.cleaned_data['database']
        # states = form.cleaned_data['states']
        # industry = form.cleaned_data['industry']
        # team = form.cleaned_data['team']
        print('loading data...')
        team = request.POST.get('team_select')
        extra = request.POST.get('true_or_false')
        keywords = request.POST.get('description')
        data = request.FILES['data']
        data = pd.read_excel(data)
        print('data loading completed.')
        list1 = keywords.split(',')
        list2 = request.POST.getlist('states')
        pages = int(request.POST.get('number'))

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        log_name = 'log.txt'
        log_path = os.path.join(BASE_DIR, log_name)
        log = open(log_path, 'a')


        log.write('bingScraper  ' + team + '  ' + keywords + '  ' + str(datetime.datetime.now()) + '  ' + 'page: ' +  str(pages) + '\n')
        log.close()
        file_name = team + ' ' + list1[0] + '.csv'
        if not os.path.exists('/Users/admin/Desktop/output/' + file_name):
            print ('Everything is good, start scraping:')
        else:
            raise Exception('A very specific bad thing happened')

        res = models.bing_grab(list1, list2, pages)
        exclude_term = exclude.exclude_term()
        for i in range(len(res)):
            res[i] = res[i].replace('https://', '').replace('http://', '').replace('www.', '').replace('\xa0', '/')
            res[i] = res[i].split('/')[0]
        res = list(set(res))

        for i in range(len(res)):
            for term in exclude_term:
                if term in res[i]:
                    res[i] = 'bad url'
        res = [x for x in res if '.com' in x or '.us' in x or '.org' in x or '.biz' in x or '.net' in x]
        if extra == 'yes':
            print ('pulling company names...')
            title = models.scraping_title(res)
            scraped_information = pd.DataFrame(pd.Series(title), columns=['scraped_information'])
            scraped_information['URLtrim'] =  res
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
        
        print ('scraping done, closing the browser...')
        time.sleep(5)
        print('Bye')
        return response




def post_upload(request):
    if request.method == 'GET':
        return render(request, 'bingScraper/bingScraper.html')
    elif request.method == 'POST':
        # No need to call post.save() at this point -- it's already saved.
        html = '<html><body><h1>scraping done</h1></body></html>'
        return HttpResponse(html)
