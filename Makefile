database:
	python3.4 manage.py makemigrations apis
	python3.4 manage.py sqlmigrate apis 0001
	python3.4 manage.py makemigrations map
	python3.4 manage.py sqlmigrate map 0001
	python3.4 manage.py makemigrations project
	python3.4 manage.py sqlmigrate project 0001
	python3.4 manage.py makemigrations login
	python3.4 manage.py sqlmigrate login 0001
	python3.4 manage.py migrate
clean:
	rm -fr apis/__pycache__
	rm -fr apis/migrations
	rm -fr login/__pycache__
	rm -fr login/migrations
	rm -fr map/__pycache__
	rm -fr map/migrations
	rm -fr project/__pycache__
	rm -fr project/migrations
