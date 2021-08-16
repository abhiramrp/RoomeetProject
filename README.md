# ROOMEET
## Help users find roommates and housings with similar interests

[Init.py creates the app and calls the bluprints](flaskr/__init__.py)

Web application created using Python Flask and SQLite. 

Created as part of 2021 Microsoft San Francisco Summer Challenge Project(SFSCP).
[Presentation link](https://docs.google.com/presentation/d/1QNUwOuXp0OwPMxWfUuRQzraDcLXTiYtdZ4gdIai7C2g/edit?usp=sharing)

###### Blueprints
[Algorthim.py](flaskr/algorithm.py) matches users with similar profiles and housings
[Auth.py](flaskr/auth.py) creates and manages user accounts
[Db.py](flaskr/db.py) manages the SQlite database
[Housing.py](flaskr/housing.py) creates and manages housing posts
[Roommeet.py](flaskr/roommeet.py) creates and manages user profiles



Please execute the following command in the terminal before starting the application
```
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
```

Execute the following command to start the application
```
$ flask run
```

If made changes to database [schema.sql](flaskr/schema.sql), please execute
```
$ flask init-db
```

Flask resource: (https://flask.palletsprojects.com/en/2.0.x/tutorial/)
