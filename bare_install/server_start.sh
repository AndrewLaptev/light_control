cd $(dirname $0)
cd ../

source .venv/bin/activate

gunicorn app:app \
    --name light_control \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    --pid gunicorn.pid \
    -D
