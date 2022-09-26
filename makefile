# Variables
admin_password = "1"
user_list_csv = "users.csv"

# Commands
create-database:
	python3 ./create-database.py ${admin_password}

load-users-from-csv:
	python3 ./load-users-into-database.py ${user_list_csv}

display-database:
	python3 ./display-database-contents.py

run:
	python3 ./main.py