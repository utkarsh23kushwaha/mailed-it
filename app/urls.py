from django.contrib import admin
from django.urls import path 
from app import views


urlpatterns = [
    path("",views.main, name='Home'),
    path("add_subscribe",views.add_subscribe, name='add_subscribe'),
    path("unsubscribe",views.unsubscribe, name='unsubscribe'),
    path("add_campaign",views.add_campaign, name='add_campaign'),
    path("send_mail",views.send_mail, name='send_mail'),
    path("success_page",views.success_page, name='success_page'),
    path("import_subscribers",views.import_subscribers, name='import_subscribers'),
    path("user_unsubscribe",views.user_unsubscribe,name="user_unsubscribe"),
    path("upload_template",views.upload_template,name='upload_template')
]
    
