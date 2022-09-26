# Dash Auth Page

Add authentication and user management to your dash app. 

### Description

This adds a user database and login page on front of your Dash app. 

You can import users from a csv file, or create them in the app itself using an admin user and going to the `/create` page.

### What Does It Look Like

The log in page:

![Login Page](./docs/login-page.png)

### Create User Page

This page is where you create users: `/create`

Roles is where you can specify the access level of the user. 

You can add as many access levels as you like, but the built in one is 'admin' or 'default'.

![Create User](./docs/create-user-page.png)

### Other Pages

After logging in user will see this page:

![After Logging In](./docs/successful-login.png)

After selecting a dash that is only available to a logged in user, they will see this page:

![Logged In Dash](./docs/logged-in-dash.png)



### How To Run This Example
_Must be run in Linux terminal, requires make_

The [makefile](./makefile) contains all the commands needed to set up and run the example dash app.


First we need to set the admin password in the [makefile](./makefile) 

This password will be used ad the first user login for the system, from which other users are created.


Create a database for users:
```bash
make create-database
```


Run the dash:
```bash
make run
```

Now you can open the dash to see the login page.


You can create users here: `/create`


### Other Useful Functions

Load a csv of users into the database.

The filename of the csv this loads can be edited in the [makefile](./makefile).

```bash
make load-users-csv
```

Check the contents of the user database:
```bash
make display-database
```

It will print a list like this:

![Display Users](./docs/display-users.png)

