

# Add a Database Table for Application Data '

And add an associated Flask form to submit data to it.

## Add Database Model for Form Data ##

in `models.py` configure AppData database object

class AppData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    item = db.Column(db.String(64), index=True,   unique=True)
    description = db.Column(db.String(140))
    value = db.Column(db.Integer)
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)


Generate the Model:
```
$ flask db migrate -m "add AppData database model"
```
and apply it to the database:

```
$ flask db upgrade
```

#### Test adding an item to AppData ####

```
python

>>> from app import db
[2019-01-14 14:44:13,450] INFO in __init__: Flask Web Application Startup
>>> from app.models import AppData
>>> item = AppData(item="a widget",description="a thing", value=25)
>>> db.session.add(item)
>>> db.session.commit()
```

#### Check item has been saved to app_data Table ####

```
$ psql -U manager base
psql (10.5)
                      ^
base=> \dt
             List of relations
 Schema |      Name       | Type  |  Owner
--------+-----------------+-------+---------
 public | alembic_version | table | manager
 public | app_data        | table | manager
 public | user            | table | manager
(3 rows)


base=> select * from app_data;
 id |         timestamp         |   item   | description | value
----+---------------------------+----------+-------------+-------
  1 | 2019-01-14 14:46:08.03277 | a widget | a thing     |    25
(1 row)
```

## Create app_data Route to Add / View App Data ##

Initially just create a form to post data - enhance later

in `routes.py`:
```
@app.route('/add_app_data', methods=['GET', 'POST'])
@login_required
def add_app_data():
    form = AddAppData()
    appData = AppData() # db model imported from models.py
    if form.validate_on_submit():
        appData.item = form.item.data
        appData.description = form.description.data
        appData.value = form.value.data

        db.session.add(appData)
        try:
            db.session.commit()
        except IntegrityError as err:   #from sqlalchemy.exc import IntegrityError

        flash('Data Integrity/Duplicate Error - changes NOT saved.', 'error')
            db.session.rollback()
            return redirect(url_for('index'))
        flash('Your changes have been saved.')
        # return redirect(url_for('edit_profile', username = user.username))
        return redirect(url_for('index'))
    return render_template('app_data.html', title='Add Data', form=form)

```

At the beginnning of `routes.py` import the Form to be used:

```
from app.forms import AddAppData
```
        
        
## Create a Form to post the App Data ##
 In `forms.py`
 
``` 
 class AddAppData(FlaskForm):
    item = TextAreaField('Item', validators=[Length(min=1, max=64)])
    description = TextAreaField('Description', validators=[Length(min=1, max=140)])
    value = DecimalField('Value')
    submit = SubmitField('Submit')
```
    
## Create a Web Template for the Form ##

```
{% extends "base.html" %}
{% import 'bootstrap/wtf.html' as wtf %}

{% block app_content %}

    <h1>Add App Data </h1>

    <form action=""  method="post">
    <div class="col-md-6">
        {{ form.hidden_tag() }}
        {{  wtf.form_field(form.item) }}
        {{  wtf.form_field(form.description) }}
        {{  wtf.form_field(form.value ) }}

        <input class="btn btn-primary" type="submit" value="Submit">

    </div>
    </form>

{% endblock %}
        
``` 

