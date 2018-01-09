"""SFA_scraper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^index/', views.index, name = 'index'),
    url(r'^$', views.home, name='home'),
    url(r'^admin/', admin.site.urls),
    url(r'^bingScraper/', include('bingScraper.urls')),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^signin/', views.signin, name = 'signin'),
    url(r'^googleScraper/', include('googleScraper.urls')),
    url(r'^logout/$', views.log_out, name = 'logout'),
    url(r'^addcompany/$', views.addCompany, name = 'add_company'),
    url(r'^check_list/', views.checklist, name = 'check_list'),
    url(r'^upload/', views.upload, name = 'upload'),
    url(r'^search_company/', views.search_company, name = 'search_company'),
    url(r'^user_management/$', views.user_management, name = 'user_management'),
    url(r'^user_management/change_user/(?P<user_id>[0-9]+)/$', views.change_user_info, name = 'change_user_info'),
    url(r'^activity_logs', views.view_logs, name = 'activity_logs'),
    url(r'^user_management/remove_user/(?P<user_id>[0-9]+)/$', views.remove_user, name = 'remove_user'),
    url(r'^clearUploadLogs', views.clearUploadLogs, name = 'clearUploadLogs'),
    url(r'^clearChecklistLogs', views.clearChecklistLogs, name = 'clearChecklistLogs'),
    url(r'^findCompany/', views.findCompany, name='findCompany'),
    url(r'^aggregate/', views.aggregate, name='aggregate')
    
]
