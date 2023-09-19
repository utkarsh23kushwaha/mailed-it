from django.db import models
from django.contrib.auth.models import User


class Campaign(models.Model):
    subject = models.TextField( null=True, blank=True)
    preview_text = models.CharField(max_length=500, null=True, blank=True)
    article_url = models.URLField(max_length=200, null=True, blank=True)
    html_content = models.TextField( null=True, blank=True)
    plain_text_content = models.TextField( null=True, blank=True)
    campaign_name = models.CharField(max_length=30, null=True, blank=True)
    published_date = models.DateField(null=True, blank=True)
    type = models.CharField(max_length=50,null=True,blank=True)
    
    def __str__(self):
        return self.campaign_name

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    Subscribed_date = models.DateField()
    Unsubscribed_date = models.DateField(null=True, blank=True)
    Status = models.CharField(max_length=20) 
    campaigns = models.ManyToManyField(Campaign)

    def __str__(self):
        return self.name


