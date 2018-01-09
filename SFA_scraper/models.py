from django.http import StreamingHttpResponse
import pandas as pd
from googleScraper.models import Company
import os
import sqlalchemy
from io import BytesIO
import datetime

columns = ['name', 'url', 'city', 'state', 'zipcode', 'owner_email', 'owner_Name', 'industry', 'datetime']
def override_upload(data):
    data.drop_duplicates(['name', 'url'], inplace=True)
    engine = sqlalchemy.create_engine('mysql+mysqldb://sfa:searchfund@sfadb.c2ytrqt7mtsh.us-east-2.rds.amazonaws.com:3306/SFA')
    database = pd.DataFrame(list(Company.objects.values_list()), columns = columns)
    df = pd.concat([database, data], ignore_index=True)
    df.drop_duplicates(subset=['name', 'url'], inplace=True, keep='last')
    df.to_sql('googleScraper_company', engine,if_exists = 'replace', index = False)

def passive_upload(data):
    data.drop_duplicates(['name', 'url'], inplace=True)
    engine = sqlalchemy.create_engine('mysql+mysqldb://sfa:searchfund@sfadb.c2ytrqt7mtsh.us-east-2.rds.amazonaws.com:3306/SFA')
    database = pd.DataFrame(list(Company.objects.values_list()), columns = columns)
    df = pd.concat([database, data], ignore_index=True)
    df.drop_duplicates(subset=['name', 'url'], inplace=True, keep='first')
    df.to_sql('googleScraper_company', engine,if_exists = 'replace', index = False)
 

def checklist(url_list):
    bio = BytesIO()
    filename = 'output.xlsx'
    data = pd.DataFrame(list(Company.objects.all().values()))
    result = data.merge(url_list, how = 'right', on = 'url')
    PandasWriter = pd.ExcelWriter(bio, engine='xlsxwriter')
    result.to_excel(PandasWriter, sheet_name=filename)
    PandasWriter.save()
    bio.seek(0)
    workbook = bio.getvalue()

    response = StreamingHttpResponse(workbook,content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename


