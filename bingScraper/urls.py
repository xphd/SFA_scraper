from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.bingScraper, name = 'bingScraper'),
    url(r'^scrapingdone/', views.scraping, name = 'bingscraping'),
    url(r'^upload/', views.post_upload, name = 'post_upload')

]