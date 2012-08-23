
INSTALL PROCEDURE
=================

pyinterp=/usr/bin/python2.7
mkvirtualenv --python=$pyinterp django14
pip install -r requirements.txt


DEMO
====

In the following installation howto, replace PROJECT_DIR with the path where you cloned the project

1*  Make a copy of the settings.py.dist file in settings.py.
2*  Edit the settings.py file adding your database settings.
3*  1*  Launch python manage.py syncdb from your PROJECT_DIR.
    2*  Answer 'yes' when asked for creating an admin user.
4*  Import PROJECT_DIR/fixtures/a_users_and_groups.json fixture with command:
        python manage.py loaddata PROJECT_DIR/fixtures/a_users_and_groups.json
5*  Run your deployement server with:
        python manage.py runserver [ip:port]
