from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from app.models import Subscriber
from app.models import Campaign
from django.contrib import messages
from django.template.loader import render_to_string
from app.utils import send_email_with_template
from django_user_agents.utils import get_user_agent
from django.contrib.auth.decorators import login_required, user_passes_test

def is_admin(user):
    return user.is_staff

def main(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'base.html'
    return render (request, template_name)

@login_required  # Ensures the user is logged in
@user_passes_test(is_admin)  # Ensures the user passes the custom test
def send_mail(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'send_mail.html'
    if request.method == 'POST':
        subject = request.POST.get('subject')
        cap = Campaign.objects.filter(subject = subject)
        for campaign in cap:
            subject = campaign.subject
            preview_text = campaign.preview_text
            article_url = campaign.article_url
            html_content = campaign.html_content
            plain_text_content = campaign.plain_text_content
            published_date = campaign.published_date
        campaign_data = {
                            'Subject': subject,
                            'preview_text': preview_text,
                            'article_url': article_url,
                            'html_content': html_content,
                            'plain_text_content': plain_text_content,
                            'published_date': published_date
                        }
        rendered_email = render_to_string('mail_template.html', context = campaign_data)
        recipients = Subscriber.objects.filter(Status='active').values_list('email', flat=True)
   
        if send_email_with_template(subject, rendered_email, recipients):
            return redirect('success_page')
        else:
            return HttpResponse("Mail Sending Failed :(")

    subjects = Campaign.objects.values_list('subject', flat=True).distinct()
    return render(request, template_name, {'subjects': subjects})

def success_page(request):
    return render(request, 'success.html')

def mobile(request):
    return render(request, 'mobile.html')

def add_subscribe(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'add_subscribe.html'
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        try:
           
            subscriber = Subscriber.objects.get(email=email)

           
            if subscriber.Status == "inactive":
                subscriber.Status = "active"
                subscriber.save()
                messages.success(request, f"Subscriber with email {email} is now active.")
            else:
                messages.error(request, f"Email {email} already exists and is active.")

        except Subscriber.DoesNotExist:
           
            date = datetime.now()
            subs = Subscriber(name=name, email=email, Subscribed_date=date.date(), Status="active", Unsubscribed_date=None)
            subs.save()
            messages.success(request, "Subscriber Added Successfully.")
    return  render(request, template_name)

def unsubscribe(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'unsubscribe.html'
    if request.method=='POST':
        email  = request.POST.get('email')
        try:
            subscriber = Subscriber.objects.get(email=email)

            if subscriber.Status == "inactive":
                messages.error(request, f"Subscriber with email {email} is already unsubscribed.")
            else:
                subscriber.Status = "inactive"
                subscriber.Unsubscribed_date = datetime.now().date()
                subscriber.save()
                messages.success(request, f"Subscriber with email {email} unsubscribed successfully.")

        except Subscriber.DoesNotExist:
            messages.error(request, f"Subscriber with email {email} not found.")
    return render (request, template_name)

def add_campaign(request):
    user_agent = get_user_agent(request)
    if user_agent.is_mobile or user_agent.is_tablet: 
        template_name = 'mobile.html'
    else : 
        template_name = 'add_campaign.html'
    if request.method=='POST':
        subject = request.POST.get('subject')
        preview_text = request.POST.get('preview_text')
        article_url = request.POST.get('article_url')
        html_content = request.POST.get('html_content')
        plain_text_content = request.POST.get('plain_text_content')
        published_date = request.POST.get('published_date')

        cap = Campaign(subject=subject,preview_text=preview_text,
                       article_url=article_url,
                       html_content=html_content,
                       plain_text_content=plain_text_content,
                       published_date=published_date)
        cap.save()


    return render (request, template_name)
