web: bin/start-pgbouncer-stunnel gunicorn -w 4 main:app --preload --timeout 60 --max-requests 500 --worker-connections 50 --worker-class gevent --graceful-timeout 60 --log-file -
