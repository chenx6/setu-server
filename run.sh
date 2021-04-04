export FLASK_APP=setu_viewer
flask run --port 8848 --host 0.0.0.0
# gunicorn -w $(nproc) -b 0.0.0.0:8848 'setu_viewer:create_app()'