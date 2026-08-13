# Django / HTMX Article Creator
This is not a standalone web app meant for production.

test it out:
- clone
- python3 -m venv venv
- **Windows**: venv/Scripts/activate      **Linux**: source venv/bin/activate
- pip install -r requirements.txt
- copy '.env.example' and rename to '.env'
- python manage.py makemigrations
- python manage.py migrate
- python manage.py loaddata sampledata
- python manage.py runserver

login is 'admin' 'admin'