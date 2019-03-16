release: flask db stamp head && flask db upgrade
web: gunicorn wsgi:app --preload