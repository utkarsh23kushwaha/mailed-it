"""
URL configuration for email_campaign_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path 
from app import views


urlpatterns = [
    path("",views.main, name='Home'),
    path("add_subscribe",views.add_subscribe, name='add_subscribe'),
    path("unsubscribe",views.unsubscribe, name='unsubscribe'),
    path("add_campaign",views.add_campaign, name='add_campaign'),
    path("send_mail",views.send_mail, name='send_mail'),
    path("success_page",views.success_page, name='success_page')
]
