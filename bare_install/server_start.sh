cd $(dirname $0)
cd ../

source .venv/bin/activate
source .env

gunicorn app:app \
    --name light_control \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:${LIGHT_CONTROL_PORT} \
    --pid gunicorn.pid \
    -D
