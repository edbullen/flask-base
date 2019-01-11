

## Base Install ##

Built and tested with Python 3.6 and Flask 1.0.2  
  
Python Dependancies listed in ./app/requirements.txt  

Requires PostgreSQL 10.6 database server   
- Install and config assume a local DB server, but a remote service is possible

## PostgreSQL Setup ##

#### Create Database and Database User ####

postgres=# CREATE DATABASE <webapp_database>;

postgres=# CREATE USER <webapp_database_user> WITH PASSWORD '<webapp_database_user_password>';

postgres=# GRANT ALL PRIVILEGES ON DATABASE base TO <webapp_database_user>;

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


