
Build a timetracker application for steps with Django admin interface
=====================================================================

Step 1
------

1. Clone the repository git://github.com/feroda/django-exercises-timetracker.git
2. Open your own branch

Step 2
------

1. Complete the model
2. Provide a basic admin interface
3. Create groups workers, managers. Managers has permission to add/change CostHolder, workers only to add/change Activity
4. Create a bunch of (staff) users of both groups
5. Export fixtures
6. Add them as fixtures NOT to be loaded at initial syncdb
7. Document it in DEMO section of INSTALL.rst

Step 3
------

1. Custom model: at each time a user MUST have an EMPTY activity for each project he belongs to
2. Custom admin interface: make activities editable in changelist

Step 4
------

1. Custom admin interface: remove start_datetime from changelist and add a button "Start/Stop"

Step 5
------

How would be the best way to provide User total delta of all his activities???

Step 6
------

1. Create a South initial migration
2. Update models CostHolder and Activity with a foreseen_datetime field blank
3. Update admin interface accordingly

