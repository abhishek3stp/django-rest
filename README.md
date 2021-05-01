# django-rest

### To run the app

```python
pip install -r requirements.txt
python manage.py runserver

```

### register & login

```python
{
    "username": "jitesh",
    "email": "jitesh@gmail.com",
    "password": "12345"
}
{
    "username": "jitesh",
    "password": "12345"
}
```

* This is a basic todo app with Token Base Authentication System with the django rest framework
* Moderator can look into Task assigned by diffrent users, When he complete's them he change **complete** status to **true**
* Users are having **CRUD** functions.

### api urls

```python
    'register   :   /register',
    'login      :   /login',
    'logout     :   /logout',
    'moderator  :   /moderator',
    'detail     :   /detail',
    'create     :   /create',
    'update     :   /update/<str:slug>/',
    'delete     :   /delete/<str:slug>/',
```

_here slug is task id_

