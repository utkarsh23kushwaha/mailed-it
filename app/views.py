from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from app.models import Subscriber
from app.models import Campaign
from django.contrib import messages
from django.template.loader import render_to_string
from app.utils import send_email_with_template
from app.utils import sheet_parser
from django_user_agents.utils import get_user_agent
from django.contrib.auth.decorators import login_required, user_passes_test
import pandas as pd
import os

cwd = os.getcwd()
template = cwd + '/templates/mail_templates/uploaded.html'


##########################################################################################################################################

def main(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'index.html'
    return render (request, template_name)

##########################################################################################################################################

def user_unsubscribe(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'add_subscribe.html'
    if request.method == 'POST':
        email  = request.POST.get('email')
        try:
            subscriber = Subscriber.objects.get(email=email)
            subscriber.Status = "inactive_by_user"
            subscriber.Unsubscribed_date = datetime.now().date()
            subscriber.save()
            messages.success(request,"Successfully_Unsubscribed")

        except Subscriber.DoesNotExist:
            messages.error(request, f"Email not found, Please Check the Email.")
    return render (request, template_name)
    

##########################################################################################################################################

def send_mail(request):
    return render(request, 'send_mail_alt.html')

##########################################################################################################################################

def success_page(request):
    return render(request, 'success.html')

##########################################################################################################################################


def import_subscribers(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'import_sheets.html'

    if request.method == 'POST':
        flag=0
        link = request.POST.get('link')
        name = request.POST.get('sheet_name')
        campaign_name = request.POST.get('campaign_name')
        data = sheet_parser(link,name)
        email_var_list = ["email","emails","e-mails","e-mail"]
        columns_list = data.columns.tolist()
  
        name = None
        try :
            for item in columns_list:
                if "name" in item.lower() and 'unnamed' not in item.lower():
                    name=item
                    
        except Exception as e:
              print("#######################ERROR:   ",e)

        email  = None
        try :
            for item in columns_list:
                if any(keyword in item.lower() for keyword in email_var_list):
                    email = item

        except Exception as e:
             print("#######################ERROR:   ",e)

        if email == None  :
            messages.error(request, "Email column Not found in the list")
        if name == None  :
            messages.error(request, "Name column Not found in the list")

            
        
        if name is not None and email is not None :
            name_list = data[name].tolist()
            print("col: ######### : ",data.columns)
            email_list = data[email].tolist()
            subscriber_list = []
            try :

                if len(name_list) == len(email_list):
                    for name , email in zip(name_list, email_list):
                        date = datetime.now()
                        try: 
                            existing_subscriber = Subscriber.objects.get(email=email)
                            subscribed_campaigns = existing_subscriber.campaigns.all()
                            
                            if campaign_name in subscribed_campaigns:
                                continue
                            else:
                                existing_subscriber.campaigns.add(Campaign.objects.get(campaign_name=campaign_name))
                                messages.success(request,f"Suscesfully Subscribed Existing Users to {campaign_name}")
                                flag=1
                                    

                        except Subscriber.DoesNotExist:
                             subs = Subscriber(name=name, email=email, Subscribed_date=date.date(), Status="active", Unsubscribed_date=None)
                             subscriber_list.append(subs)
                            
                
                else:
                    messages.error(request, "Error occured,number of names not equal to the number of emails")
            except Exception as e:
                messages.error(request, f"Error occured, check the data in your sheet__{e}")

            if len(subscriber_list)>=1:

                Subscriber.objects.bulk_create(subscriber_list)
                for sub in subscriber_list:
                    sub.campaigns.add(Campaign.objects.get(campaign_name=campaign_name))

                messages.success(request, "Subsribers sucessfully imported from Google Sheet")
    
            elif flag==1:
                pass
            elif flag==0:
                messages.success(request, "Skipped Duplicates, Import Successful")


    name_list = []
    email_list = []

    campaign_list = Campaign.objects.all().values_list("campaign_name", flat=True)
    return  render(request, template_name,{"campaigns" : campaign_list})

##########################################################################################################################################
   

def add_subscribe(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'add_subscribe.html'

    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        campaign_name = request.POST.get('campaign_name')   
        # campaign = 
        print(campaign_name)

        try:
           
            subscriber = Subscriber.objects.get(email=email)
            subscribed_campaigns = subscriber.campaigns.all()
            camps = []
            for x in subscribed_campaigns:
                camps.append(x.campaign_name)

            if campaign_name in camps:
                 if subscriber.Status == "inactive":
                    subscriber.Status = "active"
                    subscriber.save()
                    messages.success(request, f"Subscriber with email {email} is now active.")
                 else:
                     messages.error(request, f"Email {email} already exists and is active.")
            else:
                subscriber.campaigns.add(Campaign.objects.get(campaign_name=campaign_name))
                subscriber.save()
                messages.success(request, f"Sucessfully Susbcribed to {campaign_name}")

        except Subscriber.DoesNotExist:
           
            date = datetime.now()
            subs = Subscriber(name=name, email=email, Subscribed_date=date.date(), Status="active", Unsubscribed_date=None)
            subs.save()
            subs.campaigns.add(Campaign.objects.get(campaign_name=campaign_name))
            # subs.save()
            
         
            messages.success(request, "Subscriber Added Successfully.")
    campaign_list = Campaign.objects.all().values_list("campaign_name", flat=True)
    return  render(request, template_name,{"campaigns" : campaign_list})

##########################################################################################################################################


def unsubscribe(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'unsubscribe.html'
    if request.method=='POST':
        email  = request.POST.get('email')
        campaign_name = request.POST.get('campaign_name')
        try:
            subscriber = Subscriber.objects.get(email=email)

            if subscriber.Status == "inactive":
                messages.error(request, f"Subscriber with email {email} is already unsubscribed.")

            subscribed_campaigns = subscriber.campaigns.all()

            if campaign_name == 'All':
                subscriber.Status = "inactive"
                subscriber.Unsubscribed_date = datetime.now().date()
                subscriber.save()
            else:
                if campaign_name in subscribed_campaigns:
                    subscriber.campaigns.remove(Campaign.objects.get(campaign_name=campaign_name))
                    messages.success(request, f"Successfully Unsubscribed from this Campagin.")
                else :
                    messages.error(request, f"Subscriber Not subscribed to this campaign.")

        except Subscriber.DoesNotExist:
            messages.error(request, f"Subscriber with email {email} not found.")
    campaign_list = Campaign.objects.all().values_list("campaign_name", flat=True)
    return render (request, template_name,{"campaigns" : campaign_list})

##########################################################################################################################################


def upload_template(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'upload_template.html' 

    if request.method=='POST':
        date = datetime.now()
        campaign_name = request.POST.get('campaign_name')
        subject = request.POST.get('subject')
        html_content = request.POST.get('html_content')

        cap = Campaign(subject=subject,preview_text=None,
                       article_url=None,
                       html_content=html_content,
                       plain_text_content=None,
                       company_name=None,
                       published_date =date.date(),
                       campaign_name=campaign_name,
                       type="Uploaded-Template")
        cap.save()


    return render (request, template_name)


##########################################################################################################################################

def add_campaign(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'add_campaign.html'

    if request.method=='POST':
        date = datetime.now()
        subject = request.POST.get('subject')
        preview_text = request.POST.get('preview_text')
        article_url = request.POST.get('article_url')
        html_content = request.POST.get('html_content')
        plain_text_content = request.POST.get('plain_text_content')
        company_name = request.POST.get('company_name')
        campaign_name = request.POST.get('campaign_name')

        cap = Campaign(subject=subject,preview_text=preview_text,
                       article_url=article_url,
                       html_content=html_content,
                       plain_text_content=plain_text_content,
                       company_name=company_name,
                       campaign_name = campaign_name,
                       published_date =date.date(),
                       type="Form-Fill")
        cap.save()


    return render (request, template_name)

