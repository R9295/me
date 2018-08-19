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
```
./manage.py shell
```
``` python
>>> from themes.models import Theme
>>> theme = Theme.objects.create(name='NAME_HERE')
# COPY THIS UUID!
>>> print(str(theme.pk))
```


3. Create a HTML file in the folder templates/themes/. IT HAS TO BE THE <b>UUID</b> of the entry!


4. Add it to the THEME_LIST in themes/themes.py for other instances to use. <b>Important</b>


5. Thats it! You should see it in the list. Use profile previews as a way to test the theme

## How to add React.js to a theme


1. Do the above


2. Create a .js or a .jsx file in ``static/themes/`` with an appropriate name(ideally the same as the template name)

3. Add your React.js code along with the ``ReactDOM.render()`` function.


4. Add it to the webpack entry in webpack.config.js.
``` javascript
  entry: {
    index: './static/app/index',
    example: './static/themes/example'
  },
```
5. Go to the HTML file and add the following in it:
``` 
<!-- Add this bit at the beginning of the HTML file -->
{% load render_bundle from webpack_loader %}

<!-- Create your <div> which React.js is supposed to use -->
<div id="react"></div>

<!-- load the bundle(same as the name of the key in the entry dictionary), this is essentially a script tag so position accordingly -->
{% render_bundle 'example' %}
```

6. Run npm command to start watching and bundling, this has live reload!
```
npm run watch
```

7. Suggestions:

   a. webpack rebundles <b>all</b> the bundles everytime there's a change in any <b>one</b> file,for this a fix is appreciated, but in the meantime, clean the folder every now and then to save disk space!
   
   b. django-webpack-loader will give error messages in the template if the React.js build fails, if this is not verbose enough, check out the ``npm run watch`` server for more information.
   
   
# GPL-3.0
