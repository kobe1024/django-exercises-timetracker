
INSTALL PROCEDURE
=================

pyinterp=/usr/bin/python2.7
mkvirtualenv --python=$pyinterp django16
pip install -r requirements.txt


DEMO
====

Clone the repository::
    git clone git://github.com/feroda/django-exercises-timetracker.git

Open virtualenvwrapper instance::
    workon django16

Go to project directory::
    cd django-exercises-timetracker/

Initialize the database::
    python manage.py syncdb

Load data to database::
    python manage.py loaddata sample_data

Run development web server::
    python manage.py runserver

Connect with your web browser to `localhost:8000`


NOTES
-----

Export fixtures::
    python manage.py dumpdata --indent=2 auth tracker > tracker/fixtures/sample_data.json

