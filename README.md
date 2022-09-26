# Dash Auth Page

Add authentication management to your dash app. 

### Description

This adds a user database and login page on front of your Dash app. 

Users can either be created ahead of time in the user database, or creates using the user creation page.


### How To Run

The [makefile](./makefile) contains all the commands needed to set up and run the example:

_Must be run in Linux terminal, requires make_


Create a database:
```bash
make create-database
```


Run the example:
```bash
make run
```

Now create some users here: 
[Create User](http://localhost:8050/create)


Log in here:
[Login](http://localhost:8050/)


Check the contents of the user database:
```bash
make display-database
```