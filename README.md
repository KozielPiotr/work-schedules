# Overview
It's web app that lets user to create and manage work schedules. Also checks if schedule is compatibile with work law.

## Funcionalities:
- creating users accounts;
- creating workplaces;
- connecting users with workplaces;
- creating schedules for workplaces for chosen year, month and workplace;
- schedules includes workers connected to chosen workplace;
- editing existing schedules;
- creating guidelines with info how many workers should be in work each day;
- schowing changes between unaccepted and accepted versions of schedule
- loading schedule from xlsx file;
- exporting schedules to xlsx file;

Please mind that project is not yet finished and final list will have few more positions.

## Requirements:
- Linux (preferred) or Windows
- Python 3.6
- Google Chrome and [Chromedriver](http://chromedriver.chromium.org/getting-started?fbclid=IwAR3CPyq8Yr3-omfEVIHQ4X9TCJKe3bzYFGd8zbODELDSHngr04mhiuxW9hc) (for testing)
- pip

## Starting app:
1. Setup virtualenv
2. install Python libraries
```
$ pip install -r requirements.txt
```
3. Set up database
```
$ flask db upgrade
```
4. Run app
```
$ python manage.py runserver
```

## Login data
user: admin admin

password: a

## Run Robot tests
With app running:
```
$ pybot -d robot/results robot
```
Google Chrome and [Chromedriver](http://chromedriver.chromium.org/getting-started?fbclid=IwAR3CPyq8Yr3-omfEVIHQ4X9TCJKe3bzYFGd8zbODELDSHngr04mhiuxW9hc) required.

## Run unit tests
With app running:
```
$ py.test
```
Google Chrome and [Chromedriver](http://chromedriver.chromium.org/getting-started?fbclid=IwAR3CPyq8Yr3-omfEVIHQ4X9TCJKe3bzYFGd8zbODELDSHngr04mhiuxW9hc) required.
