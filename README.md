# Demo: <http://demotick.herokuapp.com/>
 
Ticketing app made with django. Track documents and task progress with email notifications and push notifications

## Features
* User friendly dashboard
* task prioritization
* Push Notifications
* In app notification
* Email task notification
* Search
* Comments on tasks
* Multiple file attachments per task (see settings)
* Multiple task assignment assignment with (select2)

## Requierements
* Django 2.0+
* Python 3.6+
* jQuery (full version, not "slim", for drag/drop prioritization0(
* JQuery DataTables
* Bootstrap (to work with provided templates, though you can override them)
* Django-notifications
* Django-pwa

## How to use it

```bash
# Get the code
git clone https://github.com/rein14/demotick.git
cd demotick

# Virtualenv modules installation (Unix based systems)
python3 -m venv venv
source ./venv/bin/activate

# Virtualenv modules installation (Windows based systems)
# virtualenv envp
# .\env\Scripts\activate

# Install modules - SQLite Storage
pip3 install -r requirements.txt

# Login
# Start the application (development mode)
python3 manage.py runserver # default port 8000

# Start the app - custom port
# python manage.py runserver 0.0.0.0:<your_port>

# Access the web app in browser: http://127.0.0.1:8000/
```
<br />
