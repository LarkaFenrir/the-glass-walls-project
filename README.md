# The Glass Walls Project

![If Slaughterhouse would have glass walls, everyone would be vegetarian.](assets/images/project-cover.png)

_**The Glass Walls Projects**_ is an interactive map to track locations and violations of slaughterhouses around the world. It is part of the [**_Karhun Henki_**](https://github.com/LarkaFenrir/karhun-henki) brand.

## Built With
Stack used to build this project (so far):   

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)

![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

## Getting Started

This project assumes you have the latest version of
- git
- Python
- Postgres with the extension PostGis (to set it up, see [documentation](https://postgis.net/documentation/getting_started/))

### Installation
This is a guide while the project is not finished.

#### 1. Clone the repo
```bash
git clone git@github.com:LarkaFenrir/the-glass-walls-project.git
```

#### 2. Create and activate a virtual environment
```bash
python -m venv env

source env/bin/activate  # On Linux/Mac

env\Scripts\activate     # On Windows
```

#### 3. Install the dependencies
```bash
pip install -r requirements.txt
```

#### 4. Create the hidden environment .env   
Take the file `.env.example` as guide.

#### 5. [Create a database in PostgreSQL](https://www.postgresql.org/docs/current/manage-ag-createdb.html)   
This assumes some knowledge of PostgreSQL, for the full documentation see [here](https://www.postgresql.org/docs/current/).   

Don't forget to run `CREATE EXTENSION postgis;` inside your database if it's not enabled by default.

#### 6. Make and run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

#### 7. Create superuser
```bash
python manage.py createsuperuser
```
#### 8. Run the server
```bash
python manage.py runserver
```
#### 9. Open the [admin panel](http://127.0.0.1:8000/admin)
#### 10. Log in with the superuser credentials you just created