from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.googleScraper, name = 'googleScraper'),
    url(r'^scrapingdone/', views.scraping, name = 'googlescraping'),

]