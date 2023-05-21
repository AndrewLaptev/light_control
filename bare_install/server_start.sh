cd $(dirname $0)
cd ../

source .venv/bin/activate
source .env

if test -f "uvicorn.pid"; then
    echo "Uvicorn already run! (PID: $(cat uvicorn.pid))"
else
    nohup uvicorn app:app \
        --host 0.0.0.0 \
        --port ${LIGHT_CONTROL_PORT} \
        >& /dev/null & echo $! > uvicorn.pid
fi
