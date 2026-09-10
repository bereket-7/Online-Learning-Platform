# Online Learning Platform

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Optional environment variables:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG` (`1` or `0`)
- `DJANGO_ALLOWED_HOSTS` (comma-separated)
- `DJANGO_EMAIL_HOST`, `DJANGO_EMAIL_PORT`, `DJANGO_DEFAULT_FROM_EMAIL`
