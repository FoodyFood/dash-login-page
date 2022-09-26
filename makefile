admin_password = "1"

create-database:
	python3 ./create-database.py ${admin_password}

display-database:
	python3 ./display-database-contents.py

run:
	python3 ./main.py