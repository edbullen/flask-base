

## Base Install ##

Built and tested with Python 3.6 and Flask 1.0.2  
  
Python Dependancies listed in ./app/requirements.txt  

Requires PostgreSQL 10.6 database server   
- Install and config assume a local DB server, but a remote service is possible

## PostgreSQL Setup ##

#### Create Database and Database User ####

`postgres=# CREATE DATABASE <webapp_database>;`

`postgres=# CREATE USER <webapp_database_user> WITH PASSWORD '<webapp_database_user_password>';`

`postgres=# GRANT ALL PRIVILEGES ON DATABASE base TO <webapp_database_user>;`

#### Setup Database Connectivity ####
  
Locate the `pg_hba.conf` file - EG:
```  
  postgres=# show hba_file;
                hba_file
  -------------------------------------
   /etc/postgresql/10/main/pg_hba.conf
  (1 row)
```
  
Confirm the location of the database - EG:
```
  postgres=# show data_directory;
         data_directory
  -----------------------------
   /var/lib/postgresql/10/main
  (1 row)
```
  
Update the `pg_hba.conf` file:
```

# TYPE  DATABASE        USER            ADDRESS                 METHOD

# IPv4 local connections:
host    all             <webapp_database_user>         127.0.0.1/0          md5

```
  
Restart database:
```
# systemctl stop postgresql
# systemctl start postgresql
```

Check Connectivity:   
```
$ psql --host=localhost -d <webapp_database> -U <webapp_database_user>  

```

## Initialise the Application Data Schema ##

Run the following *As the Flask Application UNIX user*  

 + `cd flask-base`  
 + `. ./env.sh`  
  
expected output: 
   
```
  FLASK_APP is base.py
  Please manually set MAIL_USERNAME
  Please manually set MAIL_PASSWORD
  Please manually set POSTGRES_PASSWORD
``` 

+ Set the POSTGRES_PASSWORD and Mail config as instructed - EG `export POSTGRES_PASSWORD=<webapp_database_user_password>`

Mail User/Password requires an email account to use for sending password reset emails
  
  
#### Install the FLask Linux Libraries ####

Run the following as the UNIX user `root`:
  
`# apt install python3-flask`
  
Strange Ubuntu Dependency - *As App UNIX User*:
 
`$ pip3 install psycopg2 `

```
Collecting psycopg2
  Downloading https://files.pythonhosted.org/packages/5e/d0/9e2b3ed43001ebed45caf56d5bb9d44ed3ebd68e12b87845bfa7bcd46250/psycopg2-2.7.5-cp36-cp36m-manylinux1_x86_64.whl (2.7MB)
    100% |¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦¦| 2.7MB 508kB/s
Installing collected packages: psycopg2
```
  
#### Initialise Flask ####

*As the App UNIX User*:



`$ flask db init`
  
`$ flask db migrate -m "users table" `

*typical output*
```
/home/app/.local/lib/python3.6/site-packages/psycopg2/__init__.py:144: UserWarning: The psycopg2 wheel package will be renamed from releas    e 2.8; in order to keep installing from binary please use "pip install psycopg2-binary" instead. For details see: <http://initd.org/psycop    g/docs/install.html#binary-install-from-pypi>.
  """)
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.autogenerate.compare] Detected added table 'user'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_email' on '['email']'
INFO  [alembic.autogenerate.compare] Detected added index 'ix_user_username' on '['username']'
  Generating /home/app/flask-base/migrations/versions/95d155717473_users_table.py ... done

```

#### Create the Application Data-Tables via Flask ####

`  $ flask db upgrade`


## Install Python Requirements ##

`sudo pip3 install -r requirements.txt`  
  
`sudo pip3 install psycopg2`

## Flask Upgrade ##
`pip3 install --upgrade Flask`

```
Successfully installed Flask-1.0.2
```


## Start the Application ##

`. ./env.sh`

```
FLASK_APP is base.py
Please manually set MAIL_USERNAME
Please manually set MAIL_PASSWORD
Please manually set POSTGRES_PASSWORD
```  

+ Set the POSTGRES_PASSWORD and Mail config as instructed - EG `export POSTGRES_PASSWORD=<webapp_database_user_password>`

+ Non-supported method to run on Port 80:
`# nohup flask run --host=0.0.0.0 --port=80 &`


