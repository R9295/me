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


4. Start the server
```
./manage.py runserver
```

You can login @ 127.0.0.1:8000/accounts/login

  
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
# COPY THIS UUID!
>>> print(str(theme.pk))
```


3. Create a HTML file in the folder templates/themes/. IT HAS TO BE THE <b>UUID</b> of the entry!


4. Add it to the THEME_LIST in themes/themes.py for other instances to use. <b>Important</b>


5. Thats it! You should see it in the list. Use profile previews as a way to test the theme
