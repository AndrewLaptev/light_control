cd $(dirname $0)
cd ../

kill $(cat gunicorn.pid)
