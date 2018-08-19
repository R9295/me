## me




## How to setup for development:

1. Clone the repo

```
git clone <repo>
```

(Optional) use a virtualenv

```
virtualenv venv
source venv/bin/activate
```

2. Install dependencies

```
pip3 install -r requirements.txt
npm install
```


3. Import the themes
```
./manage.py import themes
```


3. Start the server
```
./manage.py runserver
```

You can login @ 127.0.0.1:8000/accounts/login
---


## How to add a theme


1. Do the above


2. Add a theme manually with the shell
Note: the name must be relevant as it will appear in the theme select drop down list
``
./manage.py shell
``
``` python
>>> from theme.models import Theme
>>> theme = Theme.objects.create(name='NAME_HERE')
>>> print(str(theme.pk))
```
