# Django Email Campaign Manager

**Description:**

The Django Email Campaign Manager is a web application that allows you to manage email subscribers, create email campaigns, and send out email campaigns to your subscribers. This app uses an SQLite3 database for data storage. <br>
![image](https://github.com/utkarshk1607/email_campaign_manager/assets/144452025/ec2909c9-233b-4722-9131-75927eda2498)
 <br>

**Features:**

- Add and remove subscribers from your email list.
- Create and manage email campaigns.
- Start and send email campaigns to your subscribers.
- Track the status and results of your email campaigns.

**Installation:**

1. Clone the repository to your local machine: <br>
`git clone https://github.com/your-username/email-campaign-manager.git` <br>

2. Change into the project directory: <br>
`cd email-campaign-manager` <br>

3. Create a virtual environment and activate it: <br>
`python -m venv venv` <br>
`source venv/bin/activate` <br>

4. Install the required packages: <br>
`pip install -r requirements.txt` <br>

5. Apply database migrations: <br>
`python3 manage.py makemigrations` <br>
`python3 manage.py migrate` <br>

6. Create a superuser to access the admin panel: <br>
`python3 manage.py createsuperuser` <br>

7. Start the development server: <br>
`python manage.py runserver` <br>


8. Access the app at `http://l27.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin/`.

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
