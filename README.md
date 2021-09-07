# fabrique

[*Fabrique task*](test_task.md)

[*REST API documentation*](REST_API_documentation.md)



### Install and run project

- Clone from git
  
```
git clone https://github.com/ShakhzodNizamov/test_task_fabrique.git
```
- Open terminal in project repository and create virtual environment
  ```
   python3 -m venv /path/to/new/virtual/environment
  ```
- Install requirements from requirements.txt by pip

```
python -m pip install --upgrade pip
```
```
pip install -r requirements.txt
``` 

- Run migrate:

```
python manage.py migrate
```

- Create super user:

```
python manage.py createsuperuser
```

- Run project:

```
python manage.py runserver
```

