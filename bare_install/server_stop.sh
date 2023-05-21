cd $(dirname $0)
cd ../

kill $(cat uvicorn.pid)
rm uvicorn.pid
