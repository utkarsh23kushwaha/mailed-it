######################## OLDER APPROACH ##############################

# from django.core.mail import EmailMultiAlternatives
# from django.core import mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags
# from django.conf import settings

# def send_email_with_template(subject, html_content, recipients):
#     try:
#         text_content = strip_tags(html_content)
#         msg = EmailMultiAlternatives(subject, text_content, settings.EMAIL_HOST_USER, recipients)
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()
#         return True
    
#     except Exception as e:
#         print(f"Email sending failed: {str(e)}")
        # return False

######################## NEW APPROACH ##############################

import threading
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

def send_email(subject, html_content, from_email, recipients):
    try:
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(subject, text_content, from_email, recipients)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False

def send_emails_chunk(subject, html_content, from_email, chunk):

    for recipient in chunk:
        try:
            recipient_email = recipient
            send_email(subject, html_content, from_email, [recipient_email])
        except Exception as e:
            print(f"Email sending failed to {recipient_email}: {str(e)}")

def send_email_with_template(subject, html_content, recipients):
    try:
        from_email = settings.EMAIL_HOST_USER

        
        chunk_size = 3
        num_chunks = (len(recipients) + chunk_size - 1) // chunk_size

        
        chunked_recipients = [recipients[i:i + chunk_size] for i in range(0, len(recipients), chunk_size)]


        threads = []
        for chunk in chunked_recipients:
            thread = threading.Thread(target=send_emails_chunk, args=(subject, html_content, from_email, chunk))
            threads.append(thread)
            thread.start()


        for thread in threads:
            thread.join()

        print("All emails sent successfully.")
        return True
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False