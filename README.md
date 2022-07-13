
Django ticketing tracks work progress with
##Features
Drag and drop task prioritization
Email task notification
Search
Comments on tasks
Public-facing submission form for tickets
Mobile-friendly (work in progress)
Separate view for My Tasks (across lists)
Batch-import tasks via CSV
Batch-export tasks in CSV Format
Multiple file attachments per task (see settings)
Integrated mail tracking (unify a task list with an email box)

 * Bullet list
              * Nested bullet
                  * Sub-nested bullet etc
          * Bullet list item 2
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
