release: sh -c "flask db stamp head && flask db migrate && flask db upgrade"
web: gunicorn wsgi:app --preload