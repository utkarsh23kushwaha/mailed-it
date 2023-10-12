# Mail-ed It !!

**Description:**

Mail-ed it is a web application that allows you to manage email subscribers, create email campaigns, and send out email campaigns to your subscribers. This app uses an SQLite3 database for data storage. <br>
 <br>

**Features:**

- Add and remove subscribers from your email list.
- Create and manage email campaigns.
- Start and send email campaigns to your subscribers.


**Usage:**

1. **Admin Panel:**

- Access the admin panel using the superuser credentials created during installation.
- Add subscribers and manage your email list.
- Create and manage email campaigns.

2. **Endpoints:**

The app provides endpoints for managing subscribers and campaigns programmatically.

- `/add_subscribe`: add new subscribers. <br>
- `/unsubscribe`: Set status of subscribers as inactive. <br>
- `/add_campaign`: Create email campaigns. <br>
- `/send_email`: Send email of a specific campaign to all the "active users" <br>


3. **SMTP server**

For sending emails, I have used mailgun's SMTP server, you can create your own account there, and add SMTP credentials, in settings.py in order to succesfully send emails. <br>
`EMAIL_HOST = 'smtp.mailgun.org'` <br>
`EMAIL_PORT = 587` <br>
`EMAIL_HOST_USER ='your_mailgun_account_domain'` <br>
`EMAIL_HOST_PASSWORD = 'yourmailgunaccountpassword'` <br>

**Configuration:**

- The default database used is SQLite3. You can change the database settings in `settings.py` if needed.
