from models import Campaign
from jinja2 import Template

Campaigns = Campaign.objects.all()
for campaign in Campaigns:
    print(campaign.subject)


# with open('static/mail_template.html', 'r') as template_file:
#     template_string = template_file.read()

# # Create a Jinja2 template object
# template = Template(template_string)

# # Retrieve data from your database (example data)
# campaign_data = {
#     'Subject': Campaign,
#     'preview_text': 'This is a preview of the campaign email.',
#     'article_url': 'https://example.com/article',
#     'html_content': '<p>This is the HTML content of your email.</p>',
#     'plain_text_content': 'This is the plain text version of your email.',
#     'published_date': '2023-09-08',
# }

# # Render the template with the data
# rendered_email = template.render(campaign_data)