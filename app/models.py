from django.db import models

class Subscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=150)
    Subscribed_date = models.DateField()
    Unsubscribed_date = models.DateField(null=True, blank=True)
    Status = models.CharField(max_length=10)

    def __str__(self):
        return self.name
    
class Campaign(models.Model):
    subject = models.TextField()
    preview_text = models.CharField(max_length=500)
    article_url = models.URLField(max_length=200)
    html_content = models.TextField()
    plain_text_content = models.TextField()
    published_date = models.DateField()
    
    def __str__(self):
        return self.subject

